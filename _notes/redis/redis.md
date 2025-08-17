---
layout: post
title:  "Redis 整体架构"
date:   2023-06-26 10:30:15 +0800
categories: Redis
tags: Redis
permalink: /redis/redis
published: true
publish_file: 2023-06-26-redis-redis.md
toc: true
---
# Redis

本文基于Redis 7.0.11源码来分析的

## 简介

内存的key-value数据库，一般做缓存用  
[官网](https://redis.io/)  
[Github](https://github.com/redis/redis)
[作者antirez的博客](https://antirez.com/)

## 源码调试

1. `make distclean`
2. `make BUILD_WITH_DEBUG=yes -j$(nproc)`
3. 添加 `.vscode/launch.json`
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Redis Server",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/src/redis-server",
      "args": ["${workspaceFolder}/redis.conf"],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "miDebuggerPath": "/usr/bin/gdb",
      "setupCommands": [
        {
          "description": "Enable pretty-printing",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ],
      "logging": {
        "moduleLoad": true,
        "trace": true
      }
    }
  ]
}
```

## 数据类型
- Strings
- Lists
- Sets
- Hashes
- Sorted sets
- Streams 5.0
- Geospatial indexes 3.2
- Bitmaps
- Bitfields
- HyperLogLog

### Strings

### Lists

### Sets

### Hashes

### Sorted sets

### Streams

### Geospatial indexes

### Bitmaps

### Bitfields

## 数据结构

### SDS
SDS（Simple Dynamic String）

没有使用原生的c字符串，因为c的字符串是一个数组尾部\0 ，统计字符串长度的时候需要遍历数组

redis3.2之前实现的字符串数据结构

```c
struct sdshdr {
    int len; // 已使用的字节数 = 字符串长度
    int free; // 未使用的字节数
    char buf[];// 字符串本身内容 // 柔性数组
}
```

> 柔性数组定义：
> 1. 长度不固定
> 2. 结构体尾部
> 3. 动态分配内存 malloc
> 4. 连续的 可寻址 首地址+偏移量
> 其指针指向柔性数组


但是这个结构对小字符串来说，len和free所占的内存过大,后面分裂出来了5种数据类型
`sds.h`

```c
/* Note: sdshdr5 is never used, we just access the flags byte directly.
 * However is here to document the layout of type 5 SDS strings. */
struct __attribute__ ((__packed__)) sdshdr5 {
    unsigned char flags; /* 3 lsb of type, and 5 msb of string length */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr8 {
    uint8_t len; /* used */
    uint8_t alloc; /* excluding the header and null terminator */ // 申请长度/总长度
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr16 {
    uint16_t len; /* used */
    uint16_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr32 {
    uint32_t len; /* used */
    uint32_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
struct __attribute__ ((__packed__)) sdshdr64 {
    uint64_t len; /* used */
    uint64_t alloc; /* excluding the header and null terminator */
    unsigned char flags; /* 3 lsb of type, 5 unused bits */
    char buf[];
};
```

优化了 `strlen` 命令

**二进制安全的**，如果你在字符串中输入了 `\0` 字符，比如`re\0di\0s` 
这样的话你从redis里面读出来的字符串可能是`re di s`,这样就不对了，redis自己实现的sds数据结构，通过`len`参数可以很好的解决这个问题

`__attribute__ ((__packed__))` 作用： 取消二进制对齐
1. 默认情况下结构体按变量大小的最小公倍数做字节对齐
2. 取消结构体在编译过程中的优化对齐，按照实际占用字节数进行对齐
3. 带来的好处就是省内存，省空间


内存重分配

惰性释放


#### sdsnewlen

```c
sds _sdsnewlen(const void *init, size_t initlen, int trymalloc) {
    void *sh; // sds指针
    sds s; // buf
    char type = sdsReqType(initlen);// 根据长度判断使用的sdshdr类型
    /* Empty strings are usually created in order to append. Use type 8
     * since type 5 is not good at this. */
    if (type == SDS_TYPE_5 && initlen == 0) type = SDS_TYPE_8;
    int hdrlen = sdsHdrSize(type);
    unsigned char *fp; /* flags pointer. */
    size_t usable;

    assert(initlen + hdrlen + 1 > initlen); /* Catch size_t overflow */
    sh = trymalloc?
        s_trymalloc_usable(hdrlen+initlen+1, &usable) :
        s_malloc_usable(hdrlen+initlen+1, &usable);
    if (sh == NULL) return NULL;
    if (init==SDS_NOINIT)
        init = NULL;
    else if (!init)
        memset(sh, 0, hdrlen+initlen+1);
    s = (char*)sh+hdrlen;
    fp = ((unsigned char*)s)-1;
    usable = usable-hdrlen-1;
    if (usable > sdsTypeMaxSize(type))
        usable = sdsTypeMaxSize(type);
    switch(type) {
        case SDS_TYPE_5: {
            *fp = type | (initlen << SDS_TYPE_BITS);
            break;
        }
        case SDS_TYPE_8: {
            SDS_HDR_VAR(8,s);
            sh->len = initlen;
            sh->alloc = usable;
            *fp = type;
            break;
        }
        case SDS_TYPE_16: {
            SDS_HDR_VAR(16,s);
            sh->len = initlen;
            sh->alloc = usable;
            *fp = type;
            break;
        }
        case SDS_TYPE_32: {
            SDS_HDR_VAR(32,s);
            sh->len = initlen;
            sh->alloc = usable;
            *fp = type;
            break;
        }
        case SDS_TYPE_64: {
            SDS_HDR_VAR(64,s);
            sh->len = initlen;
            sh->alloc = usable;
            *fp = type;
            break;
        }
    }
    if (initlen && init)
        memcpy(s, init, initlen);
    s[initlen] = '\0';
    return s;
}
```

#### sdsfree

```c
void sdsfree(sds s) {
    if (s == NULL) return;
    s_free((char*)s-sdsHdrSize(s[-1]));
}
```

#### sdscatlen

```c
sds sdscatlen(sds s, const void *t, size_t len) {
    size_t curlen = sdslen(s);

    s = sdsMakeRoomFor(s,len); // 判断拼接后的字符串是否需要扩容
    if (s == NULL) return NULL;
    memcpy(s+curlen, t, len);
    sdssetlen(s, curlen+len);
    s[curlen+len] = '\0';
    return s;
}

```

#### sdsMakeRoomFor
字符串扩容

1. 活动当前sds可用空间avail，若大于等于新增长度addlen则无需扩容，直接返回
2. 若avali小于addlen，len + addlen < 1M,则2倍扩容
3. 若avali小于addlen，len + addlen >= 1M,则 +1M扩容
4. 根据新长度选择sds类型，如果sds类型和原类型相同，则通过realloc扩大柔性数组
5. 如果sds类型和原类型不相同，则malloc重新申请内存，并把原buf内容移动到新位置

```c
sds _sdsMakeRoomFor(sds s, size_t addlen, int greedy) {
    void *sh, *newsh;
    size_t avail = sdsavail(s);
    size_t len, newlen, reqlen;
    char type, oldtype = s[-1] & SDS_TYPE_MASK;
    int hdrlen;
    size_t usable;

    /* Return ASAP if there is enough space left. */
    if (avail >= addlen) return s;

    len = sdslen(s);
    sh = (char*)s-sdsHdrSize(oldtype);
    reqlen = newlen = (len+addlen);
    assert(newlen > len);   /* Catch size_t overflow */
    if (greedy == 1) {
        if (newlen < SDS_MAX_PREALLOC)
            newlen *= 2;
        else
            newlen += SDS_MAX_PREALLOC;
    }

    type = sdsReqType(newlen);

    /* Don't use type 5: the user is appending to the string and type 5 is
     * not able to remember empty space, so sdsMakeRoomFor() must be called
     * at every appending operation. */
    if (type == SDS_TYPE_5) type = SDS_TYPE_8;

    hdrlen = sdsHdrSize(type);
    assert(hdrlen + newlen + 1 > reqlen);  /* Catch size_t overflow */
    if (oldtype==type) {
        newsh = s_realloc_usable(sh, hdrlen+newlen+1, &usable);
        if (newsh == NULL) return NULL;
        s = (char*)newsh+hdrlen;
    } else {
        /* Since the header size changes, need to move the string forward,
         * and can't use realloc */
        newsh = s_malloc_usable(hdrlen+newlen+1, &usable);
        if (newsh == NULL) return NULL;
        memcpy((char*)newsh+hdrlen, s, len+1);
        s_free(sh);
        s = (char*)newsh+hdrlen;
        s[-1] = type;
        sdssetlen(s, len);
    }
    usable = usable-hdrlen-1;
    if (usable > sdsTypeMaxSize(type))
        usable = sdsTypeMaxSize(type);
    sdssetalloc(s, usable);
    return s;
}
```


#### SDS的编码

1. OBJ_ENCODING_EMBSTR 短字串编码
2. OBJ_ENCODING_RAW 普通字串编码
3. OBJ_ENCODING_INT 整型数字编码

```c
#define OBJ_ENCODING_EMBSTR_SIZE_LIMIT 44
robj *createStringObject(const char *ptr, size_t len) {
    if (len <= OBJ_ENCODING_EMBSTR_SIZE_LIMIT)
        return createEmbeddedStringObject(ptr,len);
    else
        return createRawStringObject(ptr,len);
}
```


```c
/* Try to encode a string object in order to save space */
robj *tryObjectEncoding(robj *o) {
    long value;
    sds s = o->ptr;
    size_t len;

    /* Make sure this is a string object, the only type we encode
     * in this function. Other types use encoded memory efficient
     * representations but are handled by the commands implementing
     * the type. */
    serverAssertWithInfo(NULL,o,o->type == OBJ_STRING);

    /* We try some specialized encoding only for objects that are
     * RAW or EMBSTR encoded, in other words objects that are still
     * in represented by an actually array of chars. */
    if (!sdsEncodedObject(o)) return o;

    /* It's not safe to encode shared objects: shared objects can be shared
     * everywhere in the "object space" of Redis and may end in places where
     * they are not handled. We handle them only as values in the keyspace. */
     if (o->refcount > 1) return o;

    /* Check if we can represent this string as a long integer.
     * Note that we are sure that a string larger than 20 chars is not
     * representable as a 32 nor 64 bit integer. */
    len = sdslen(s);
    if (len <= 20 && string2l(s,len,&value)) {
        /* This object is encodable as a long. Try to use a shared object.
         * Note that we avoid using shared integers when maxmemory is used
         * because every object needs to have a private LRU field for the LRU
         * algorithm to work well. */
        if ((server.maxmemory == 0 ||
            !(server.maxmemory_policy & MAXMEMORY_FLAG_NO_SHARED_INTEGERS)) &&
            value >= 0 &&
            value < OBJ_SHARED_INTEGERS)
        {
            decrRefCount(o);
            incrRefCount(shared.integers[value]);
            return shared.integers[value];
        } else {
            if (o->encoding == OBJ_ENCODING_RAW) {
                sdsfree(o->ptr);
                o->encoding = OBJ_ENCODING_INT;
                o->ptr = (void*) value;
                return o;
            } else if (o->encoding == OBJ_ENCODING_EMBSTR) {
                decrRefCount(o);
                return createStringObjectFromLongLongForValue(value);
            }
        }
    }

    /* If the string is small and is still RAW encoded,
     * try the EMBSTR encoding which is more efficient.
     * In this representation the object and the SDS string are allocated
     * in the same chunk of memory to save space and cache misses. */
    if (len <= OBJ_ENCODING_EMBSTR_SIZE_LIMIT) {
        robj *emb;

        if (o->encoding == OBJ_ENCODING_EMBSTR) return o;
        emb = createEmbeddedStringObject(s,sdslen(s));
        decrRefCount(o);
        return emb;
    }

    /* We can't encode the object...
     *
     * Do the last try, and at least optimize the SDS string inside
     * the string object to require little space, in case there
     * is more than 10% of free space at the end of the SDS string.
     *
     * We do that only for relatively large strings as this branch
     * is only entered if the length of the string is greater than
     * OBJ_ENCODING_EMBSTR_SIZE_LIMIT. */
    trimStringObjectIfNeeded(o);

    /* Return the original object. */
    return o;
}

```


#### SDS的一些优势

1. 获得len、free、alloc的时间为O(1)
2. 二进制安全，可以存储二进制数据
3. 在可能造成缓冲区溢出时会自动重新分配内存，杜绝了buf[]溢出


### skiplist
跳表实现的
`server.h`
```c
/* ZSETs use a specialized version of Skiplists */
typedef struct zskiplistNode {
    sds ele; // 字符串
    double score; // 得分
    struct zskiplistNode *backward; // 上一个元素的指针
    struct zskiplistLevel {
        struct zskiplistNode *forward; // 下一个元素的指针
        unsigned long span; // 本节点到下个节点跳过的节点数量
    } level[];
} zskiplistNode;

typedef struct zskiplist {
    struct zskiplistNode *header, *tail;
    // 元素数量
    unsigned long length;
    // 最高层数
    int level;
} zskiplist;

typedef struct zset {
    dict *dict;
    zskiplist *zsl;
} zset;
```


#### 创建跳跃表
`t_zset.c`文件
```c
/* Create a new skiplist. */
zskiplist *zslCreate(void) {
    int j;
    zskiplist *zsl;

    zsl = zmalloc(sizeof(*zsl)); // 分配内存
    zsl->level = 1;
    zsl->length = 0;
    zsl->header = zslCreateNode(ZSKIPLIST_MAXLEVEL,0,NULL);
    for (j = 0; j < ZSKIPLIST_MAXLEVEL; j++) {
        zsl->header->level[j].forward = NULL;
        zsl->header->level[j].span = 0;
    }
    zsl->header->backward = NULL;
    zsl->tail = NULL;
    return zsl;
}
```

#### zslGetRank

```c
/* Find the rank for an element by both score and key.
 * Returns 0 when the element cannot be found, rank otherwise.
 * Note that the rank is 1-based due to the span of zsl->header to the
 * first element. */
unsigned long zslGetRank(zskiplist *zsl, double score, sds ele) {
    zskiplistNode *x;
    unsigned long rank = 0;
    int i;

    x = zsl->header;
    for (i = zsl->level-1; i >= 0; i--) {
        while (x->level[i].forward &&
            (x->level[i].forward->score < score ||
                (x->level[i].forward->score == score &&
                sdscmp(x->level[i].forward->ele,ele) <= 0))) {
            rank += x->level[i].span;
            x = x->level[i].forward;
        }

        /* x might be equal to zsl->header, so test if obj is non-NULL */
        if (x->ele && x->score == score && sdscmp(x->ele,ele) == 0) {
            return rank;
        }
    }
    return 0;
}
```

#### zslGetElementByRank
```c
/* Finds an element by its rank. The rank argument needs to be 1-based. */
zskiplistNode* zslGetElementByRank(zskiplist *zsl, unsigned long rank) {
    zskiplistNode *x;
    unsigned long traversed = 0;
    int i;

    x = zsl->header;
    for (i = zsl->level-1; i >= 0; i--) {
        while (x->level[i].forward && (traversed + x->level[i].span) <= rank)
        {
            traversed += x->level[i].span;
            x = x->level[i].forward;
        }
        if (traversed == rank) {
            return x;
        }
    }
    return NULL;
}
```


#### zslInsert
```c
/* Insert a new node in the skiplist. Assumes the element does not already
 * exist (up to the caller to enforce that). The skiplist takes ownership
 * of the passed SDS string 'ele'. */
zskiplistNode *zslInsert(zskiplist *zsl, double score, sds ele) {
    zskiplistNode *update[ZSKIPLIST_MAXLEVEL], *x;
    unsigned long rank[ZSKIPLIST_MAXLEVEL];
    int i, level;

    serverAssert(!isnan(score));
    x = zsl->header;
    for (i = zsl->level-1; i >= 0; i--) {
        /* store rank that is crossed to reach the insert position */
        rank[i] = i == (zsl->level-1) ? 0 : rank[i+1];
        while (x->level[i].forward &&
                (x->level[i].forward->score < score ||
                    (x->level[i].forward->score == score &&
                    sdscmp(x->level[i].forward->ele,ele) < 0)))
        {
            rank[i] += x->level[i].span;
            x = x->level[i].forward;
        }
        update[i] = x;
    }
    /* we assume the element is not already inside, since we allow duplicated
     * scores, reinserting the same element should never happen since the
     * caller of zslInsert() should test in the hash table if the element is
     * already inside or not. */
    level = zslRandomLevel();
    if (level > zsl->level) {
        for (i = zsl->level; i < level; i++) {
            rank[i] = 0;
            update[i] = zsl->header;
            update[i]->level[i].span = zsl->length;
        }
        zsl->level = level;
    }
    x = zslCreateNode(level,score,ele);
    for (i = 0; i < level; i++) {
        x->level[i].forward = update[i]->level[i].forward;
        update[i]->level[i].forward = x;

        /* update span covered by update[i] as x is inserted here */
        x->level[i].span = update[i]->level[i].span - (rank[0] - rank[i]);
        update[i]->level[i].span = (rank[0] - rank[i]) + 1;
    }

    /* increment span for untouched levels */
    for (i = level; i < zsl->level; i++) {
        update[i]->level[i].span++;
    }

    x->backward = (update[0] == zsl->header) ? NULL : update[0];
    if (x->level[0].forward)
        x->level[0].forward->backward = x;
    else
        zsl->tail = x;
    zsl->length++;
    return x;
}
```


#### zsldelete
```c
/* Delete an element with matching score/element from the skiplist.
 * The function returns 1 if the node was found and deleted, otherwise
 * 0 is returned.
 *
 * If 'node' is NULL the deleted node is freed by zslFreeNode(), otherwise
 * it is not freed (but just unlinked) and *node is set to the node pointer,
 * so that it is possible for the caller to reuse the node (including the
 * referenced SDS string at node->ele). */
int zslDelete(zskiplist *zsl, double score, sds ele, zskiplistNode **node) {
    zskiplistNode *update[ZSKIPLIST_MAXLEVEL], *x;
    int i;

    x = zsl->header;
    for (i = zsl->level-1; i >= 0; i--) {
        while (x->level[i].forward &&
                (x->level[i].forward->score < score ||
                    (x->level[i].forward->score == score &&
                     sdscmp(x->level[i].forward->ele,ele) < 0)))
        {
            x = x->level[i].forward;
        }
        update[i] = x;
    }
    /* We may have multiple elements with the same score, what we need
     * is to find the element with both the right score and object. */
    x = x->level[0].forward;
    if (x && score == x->score && sdscmp(x->ele,ele) == 0) {
        zslDeleteNode(zsl, x, update);
        if (!node)
            zslFreeNode(x);
        else
            *node = x;
        return 1;
    }
    return 0; /* not found */
}
```


### ziplist
`ziplist.c`

```c


/* We use this function to receive information about a ziplist entry.
 * Note that this is not how the data is actually encoded, is just what we
 * get filled by a function in order to operate more easily. */
typedef struct zlentry {
    unsigned int prevrawlensize; /* Bytes used to encode the previous entry len*/
    unsigned int prevrawlen;     /* Previous entry len. */
    unsigned int lensize;        /* Bytes used to encode this entry type/len.
                                    For example strings have a 1, 2 or 5 bytes
                                    header. Integers always use a single byte.*/
    unsigned int len;            /* Bytes used to represent the actual entry.
                                    For strings this is just the string length
                                    while for integers it is 1, 2, 3, 4, 8 or
                                    0 (for 4 bit immediate) depending on the
                                    number range. */
    unsigned int headersize;     /* prevrawlensize + lensize. */
    unsigned char encoding;      /* Set to ZIP_STR_* or ZIP_INT_* depending on
                                    the entry encoding. However for 4 bits
                                    immediate integers this can assume a range
                                    of values and must be range-checked. */
    unsigned char *p;            /* Pointer to the very start of the entry, that
                                    is, this points to prev-entry-len field. */
} zlentry;
```


`<zlbytes> <zltail> <zllen> <entry> <entry> ... <entry> <zlend>`
- NOTE: all fields are stored in little endian, if not specified otherwise.

- zlbytes, uint32_t, is an unsigned integer to hold the number of bytes that the ziplist occupies including the four bytes of the zlbytes field itself.
- zltail,uint32_t, is the offset to the last entry in the list, base 0
- zllen,uint16_t,is the number of entries, When there are more than 2^16-2 entries, this value is set to 2^16-1 and we need to traverse the entire list to know how many items it holds.
- zlend,uint8_t,is a special entry representing the end of the ziplist.Is encoded as a single byte equal to 255. No other normal entry starts with a byte set to the value of 255.

每个`entry`的内部结构
`<prevlen> <encoding> <entry-data>`


来一个实际的例子:

```txt
[0f 00 00 00] [0c 00 00 00] [02 00] [00 f3] [02 f6] [ff]
      |             |          |       |       |     |
   zlbytes        zltail    entries   "2"     "5"   end
```


#### ziplistNew

#### ziplistInsert

#### ziplistDelete

#### ziplistFind

#### 设计思想和优势
1. 主要思想就是压缩内存
2. 连续的内存，元素与元素之间没有空隙
3. encoding即存类别也存长度
4. 典型的时间换空间的思想


### dict

应用：
1. Redis主存储
2. hash数据类型的实现
3. 过期时间的key、zset中value和score的映射关系

源码文件`dict.h`,`dict.c`


```c
struct dict {
    dictType *type;

    dictEntry **ht_table[2];
    unsigned long ht_used[2];

    long rehashidx; /* rehashing not in progress if rehashidx == -1 */

    /* Keep small vars at end for optimal (minimal) struct padding */
    int16_t pauserehash; /* If >0 rehashing is paused (<0 indicates coding error) */
    signed char ht_size_exp[2]; /* exponent of size. (size = 1<<exp) */
};


typedef struct dictType {
    uint64_t (*hashFunction)(const void *key);
    void *(*keyDup)(dict *d, const void *key);
    void *(*valDup)(dict *d, const void *obj);
    int (*keyCompare)(dict *d, const void *key1, const void *key2);
    void (*keyDestructor)(dict *d, void *key);
    void (*valDestructor)(dict *d, void *obj);
    int (*expandAllowed)(size_t moreMem, double usedRatio);
    /* Allow a dictEntry to carry extra caller-defined metadata.  The
     * extra memory is initialized to 0 when a dictEntry is allocated. */
    size_t (*dictEntryMetadataBytes)(dict *d);
} dictType;

typedef struct dictEntry {
    void *key;
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
        double d;
    } v;
    struct dictEntry *next;     /* Next entry in the same hash bucket. */
    void *metadata[];           /* An arbitrary number of bytes (starting at a
                                 * pointer-aligned address) of size as returned
                                 * by dictType's dictEntryMetadataBytes(). */
} dictEntry;
```

#### hash函数

1. 客户端： murmurhash
2. 服务端： siphash


#### dictCreate
```c
/* Create a new hash table */
dict *dictCreate(dictType *type)
{
    dict *d = zmalloc(sizeof(*d));

    _dictInit(d,type);
    return d;
}

/* Initialize the hash table */
int _dictInit(dict *d, dictType *type)
{
    _dictReset(d, 0);
    _dictReset(d, 1);
    d->type = type;
    d->rehashidx = -1;
    d->pauserehash = 0;
    return DICT_OK;
}
```

#### dictFind
```c
dictEntry *dictFind(dict *d, const void *key)
{
    dictEntry *he;
    uint64_t h, idx, table;

    if (dictSize(d) == 0) return NULL; /* dict is empty */
    if (dictIsRehashing(d)) _dictRehashStep(d);
    h = dictHashKey(d, key);
    for (table = 0; table <= 1; table++) {
        idx = h & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        he = d->ht_table[table][idx];
        while(he) {
            if (key==he->key || dictCompareKeys(d, key, he->key))
                return he;
            he = he->next;
        }
        if (!dictIsRehashing(d)) return NULL;
    }
    return NULL;
}
```


#### dictAdd
```c
/* Add an element to the target hash table */
int dictAdd(dict *d, void *key, void *val)
{
    dictEntry *entry = dictAddRaw(d,key,NULL);

    if (!entry) return DICT_ERR;
    dictSetVal(d, entry, val);
    return DICT_OK;
}
/* Low level add or find:
 * This function adds the entry but instead of setting a value returns the
 * dictEntry structure to the user, that will make sure to fill the value
 * field as they wish.
 *
 * This function is also directly exposed to the user API to be called
 * mainly in order to store non-pointers inside the hash value, example:
 *
 * entry = dictAddRaw(dict,mykey,NULL);
 * if (entry != NULL) dictSetSignedIntegerVal(entry,1000);
 *
 * Return values:
 *
 * If key already exists NULL is returned, and "*existing" is populated
 * with the existing entry if existing is not NULL.
 *
 * If key was added, the hash entry is returned to be manipulated by the caller.
 */
dictEntry *dictAddRaw(dict *d, void *key, dictEntry **existing)
{
    long index;
    dictEntry *entry;
    int htidx;

    if (dictIsRehashing(d)) _dictRehashStep(d);

    /* Get the index of the new element, or -1 if
     * the element already exists. */
    if ((index = _dictKeyIndex(d, key, dictHashKey(d,key), existing)) == -1)
        return NULL;

    /* Allocate the memory and store the new entry.
     * Insert the element in top, with the assumption that in a database
     * system it is more likely that recently added entries are accessed
     * more frequently. */
    htidx = dictIsRehashing(d) ? 1 : 0;
    size_t metasize = dictMetadataSize(d);
    entry = zmalloc(sizeof(*entry) + metasize);
    if (metasize > 0) {
        memset(dictMetadata(entry), 0, metasize);
    }
    entry->next = d->ht_table[htidx][index];
    d->ht_table[htidx][index] = entry;
    d->ht_used[htidx]++;

    /* Set the hash entry fields. */
    dictSetKey(d, entry, key);
    return entry;
}
```
#### dictReplace

#### dictDelete

```c
/* Remove an element, returning DICT_OK on success or DICT_ERR if the
 * element was not found. */
int dictDelete(dict *ht, const void *key) {
    return dictGenericDelete(ht,key,0) ? DICT_OK : DICT_ERR;
}

/* Search and remove an element. This is a helper function for
 * dictDelete() and dictUnlink(), please check the top comment
 * of those functions. */
static dictEntry *dictGenericDelete(dict *d, const void *key, int nofree) {
    uint64_t h, idx;
    dictEntry *he, *prevHe;
    int table;

    /* dict is empty */
    if (dictSize(d) == 0) return NULL;

    if (dictIsRehashing(d)) _dictRehashStep(d);
    h = dictHashKey(d, key);

    for (table = 0; table <= 1; table++) {
        idx = h & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        he = d->ht_table[table][idx];
        prevHe = NULL;
        while(he) {
            if (key==he->key || dictCompareKeys(d, key, he->key)) {
                /* Unlink the element from the list */
                if (prevHe)
                    prevHe->next = he->next;
                else
                    d->ht_table[table][idx] = he->next;
                if (!nofree) {
                    dictFreeUnlinkedEntry(d, he);
                }
                d->ht_used[table]--;
                return he;
            }
            prevHe = he;
            he = he->next;
        }
        if (!dictIsRehashing(d)) break;
    }
    return NULL; /* not found */
}
```

#### 渐进式rehash
redis设计了一种rehash的流程是分步骤的，并不会在第一次出发rehash的时候把所有的bucket都处理完毕，而是每次访问字典的时候处理。这样做的好处是如果dict非常大的时候，整个rehash的处理时间都分摊开了。并不会
阻塞redis的单线程。非常漂亮的处理逻辑。
```c
/* Performs N steps of incremental rehashing. Returns 1 if there are still
 * keys to move from the old to the new hash table, otherwise 0 is returned.
 *
 * Note that a rehashing step consists in moving a bucket (that may have more
 * than one key as we use chaining) from the old to the new hash table, however
 * since part of the hash table may be composed of empty spaces, it is not
 * guaranteed that this function will rehash even a single bucket, since it
 * will visit at max N*10 empty buckets in total, otherwise the amount of
 * work it does would be unbound and the function may block for a long time. */
int dictRehash(dict *d, int n) {
    int empty_visits = n*10; /* Max number of empty buckets to visit. */
    if (dict_can_resize == DICT_RESIZE_FORBID || !dictIsRehashing(d)) return 0;
    if (dict_can_resize == DICT_RESIZE_AVOID && 
        (DICTHT_SIZE(d->ht_size_exp[1]) / DICTHT_SIZE(d->ht_size_exp[0]) < dict_force_resize_ratio))
    {
        return 0;
    }

    while(n-- && d->ht_used[0] != 0) {
        dictEntry *de, *nextde;

        /* Note that rehashidx can't overflow as we are sure there are more
         * elements because ht[0].used != 0 */
        assert(DICTHT_SIZE(d->ht_size_exp[0]) > (unsigned long)d->rehashidx);
        while(d->ht_table[0][d->rehashidx] == NULL) {
            d->rehashidx++;
            if (--empty_visits == 0) return 1;
        }
        de = d->ht_table[0][d->rehashidx];
        /* Move all the keys in this bucket from the old to the new hash HT */
        while(de) {
            uint64_t h;

            nextde = de->next;
            /* Get the index in the new hash table */
            h = dictHashKey(d, de->key) & DICTHT_SIZE_MASK(d->ht_size_exp[1]);
            de->next = d->ht_table[1][h];
            d->ht_table[1][h] = de;
            d->ht_used[0]--;
            d->ht_used[1]++;
            de = nextde;
        }
        d->ht_table[0][d->rehashidx] = NULL;
        d->rehashidx++;
    }

    /* Check if we already rehashed the whole table... */
    if (d->ht_used[0] == 0) {
        zfree(d->ht_table[0]);
        /* Copy the new ht onto the old one */
        d->ht_table[0] = d->ht_table[1];
        d->ht_used[0] = d->ht_used[1];
        d->ht_size_exp[0] = d->ht_size_exp[1];
        _dictReset(d, 1);
        d->rehashidx = -1;
        return 0;
    }

    /* More to rehash... */
    return 1;
}

/* Resize the table to the minimal size that contains all the elements,
 * but with the invariant of a USED/BUCKETS ratio near to <= 1 */
int dictResize(dict *d)
{
    unsigned long minimal;

    if (dict_can_resize != DICT_RESIZE_ENABLE || dictIsRehashing(d)) return DICT_ERR;
    minimal = d->ht_used[0];
    if (minimal < DICT_HT_INITIAL_SIZE)
        minimal = DICT_HT_INITIAL_SIZE;
    return dictExpand(d, minimal);
}
```

#### 字典的遍历

```c
/* If safe is set to 1 this is a safe iterator, that means, you can call
 * dictAdd, dictFind, and other functions against the dictionary even while
 * iterating. Otherwise it is a non safe iterator, and only dictNext()
 * should be called while iterating. */
typedef struct dictIterator {
    dict *d;
    long index;
    int table, safe;
    dictEntry *entry, *nextEntry;
    /* unsafe iterator fingerprint for misuse detection. */
    unsigned long long fingerprint;
} dictIterator;
```

#### 设计思想和优势

### intset
```c
typedef struct intset {
    uint32_t encoding;
    uint32_t length;
    int8_t contents[];
} intset;
```

#### intsetNew
```c
/* Create an empty intset. */
intset *intsetNew(void) {
    intset *is = zmalloc(sizeof(intset));
    is->encoding = intrev32ifbe(INTSET_ENC_INT16);
    is->length = 0;
    return is;
}
```

#### intsetFind

```c
/* Determine whether a value belongs to this set */
uint8_t intsetFind(intset *is, int64_t value) {
    uint8_t valenc = _intsetValueEncoding(value);
    return valenc <= intrev32ifbe(is->encoding) && intsetSearch(is,value,NULL);
}

/* Search for the position of "value". Return 1 when the value was found and
 * sets "pos" to the position of the value within the intset. Return 0 when
 * the value is not present in the intset and sets "pos" to the position
 * where "value" can be inserted. */
static uint8_t intsetSearch(intset *is, int64_t value, uint32_t *pos) {
    int min = 0, max = intrev32ifbe(is->length)-1, mid = -1;
    int64_t cur = -1;

    /* The value can never be found when the set is empty */
    if (intrev32ifbe(is->length) == 0) {
        if (pos) *pos = 0;
        return 0;
    } else {
        /* Check for the case where we know we cannot find the value,
         * but do know the insert position. */
        if (value > _intsetGet(is,max)) {
            if (pos) *pos = intrev32ifbe(is->length);
            return 0;
        } else if (value < _intsetGet(is,0)) {
            if (pos) *pos = 0;
            return 0;
        }
    }

    while(max >= min) {
        mid = ((unsigned int)min + (unsigned int)max) >> 1;
        cur = _intsetGet(is,mid);
        if (value > cur) {
            min = mid+1;
        } else if (value < cur) {
            max = mid-1;
        } else {
            break;
        }
    }

    if (value == cur) {
        if (pos) *pos = mid;
        return 1;
    } else {
        if (pos) *pos = min;
        return 0;
    }
}
```

#### intsetAdd

```c
/* Insert an integer in the intset */
intset *intsetAdd(intset *is, int64_t value, uint8_t *success) {
    uint8_t valenc = _intsetValueEncoding(value);
    uint32_t pos;
    if (success) *success = 1;

    /* Upgrade encoding if necessary. If we need to upgrade, we know that
     * this value should be either appended (if > 0) or prepended (if < 0),
     * because it lies outside the range of existing values. */
    if (valenc > intrev32ifbe(is->encoding)) {
        /* This always succeeds, so we don't need to curry *success. */
        return intsetUpgradeAndAdd(is,value);
    } else {
        /* Abort if the value is already present in the set.
         * This call will populate "pos" with the right position to insert
         * the value when it cannot be found. */
        if (intsetSearch(is,value,&pos)) {
            if (success) *success = 0;
            return is;
        }

        is = intsetResize(is,intrev32ifbe(is->length)+1);
        if (pos < intrev32ifbe(is->length)) intsetMoveTail(is,pos,pos+1);
    }

    _intsetSet(is,pos,value);
    is->length = intrev32ifbe(intrev32ifbe(is->length)+1);
    return is;
}

/* Upgrades the intset to a larger encoding and inserts the given integer. */
static intset *intsetUpgradeAndAdd(intset *is, int64_t value) {
    uint8_t curenc = intrev32ifbe(is->encoding);
    uint8_t newenc = _intsetValueEncoding(value);
    int length = intrev32ifbe(is->length);
    int prepend = value < 0 ? 1 : 0;

    /* First set new encoding and resize */
    is->encoding = intrev32ifbe(newenc);
    is = intsetResize(is,intrev32ifbe(is->length)+1);

    /* Upgrade back-to-front so we don't overwrite values.
     * Note that the "prepend" variable is used to make sure we have an empty
     * space at either the beginning or the end of the intset. */
    while(length--)
        _intsetSet(is,length+prepend,_intsetGetEncoded(is,length,curenc));

    /* Set the value at the beginning or the end. */
    if (prepend)
        _intsetSet(is,0,value);
    else
        _intsetSet(is,intrev32ifbe(is->length),value);
    is->length = intrev32ifbe(intrev32ifbe(is->length)+1);
    return is;
}
```

#### intsetRemove
```c
/* Delete integer from intset */
intset *intsetRemove(intset *is, int64_t value, int *success) {
    uint8_t valenc = _intsetValueEncoding(value);
    uint32_t pos;
    if (success) *success = 0;

    if (valenc <= intrev32ifbe(is->encoding) && intsetSearch(is,value,&pos)) {
        uint32_t len = intrev32ifbe(is->length);

        /* We know we can delete */
        if (success) *success = 1;

        /* Overwrite value with tail and update length */
        if (pos < (len-1)) intsetMoveTail(is,pos+1,pos);
        is = intsetResize(is,len-1);
        is->length = intrev32ifbe(len-1);
    }
    return is;
}
```

### quickList

redis3.2之前是用ziplist或双向链表实现的list

但是链表有几个问题：
1. 每个节点都有上一个节点和下一个节点的指针，指针不存储数据但是会占用内存,节点多了之后会造成很大的内存浪费
2. 链表的每个节点在内存上是单独分配的，导致内存内存碎片化，对CPU缓存也不太友好

ziplist也有几个问题：
1. 插入/删除元素慢

为了平衡两者的优点，quickList使用了ziplist+双向链表结合的数据结构

7.0之后使用的双向链表 + listpack的数据结构

list的底层实现
`quickList.c`，`quickList.h`
```c
/* Optimization levels for size-based filling.
 * Note that the largest possible limit is 64k, so even if each record takes
 * just one byte, it still won't overflow the 16 bit count field. */
static const size_t optimization_level[] = {4096, 8192, 16384, 32768, 65536};

typedef struct quicklist {
    quicklistNode *head;        // 头节点
    quicklistNode *tail;        // 尾节点
    unsigned long count;        /* total count of all entries in all listpacks */
    unsigned long len;          /* number of quicklistNodes */
    /**
    可以是负值，代表了一种特殊的策略，是用节点的大小限制的，从-1开始对应的上面的optimization_level
    */
    signed int fill : QL_FILL_BITS;       /* fill factor for individual nodes */  // 每个节点的“填充因子”配置，控制 listpack 中最多放多少个元素或占多大空间（压缩策略的一部分）
    unsigned int compress : QL_COMP_BITS; /* depth of end nodes not to compress;0=off */ // 表示 quicklist 两端不压缩的节点数量，中间节点可能会被压缩成 LZF 格式
    unsigned int bookmark_count: QL_BM_BITS;
    quicklistBookmark bookmarks[];
} quicklist;

typedef struct quicklistNode {
    struct quicklistNode *prev; // 上一个节点
    struct quicklistNode *next; // 下一个节点
    unsigned char *entry; // quicklistEntry listpack
    size_t sz;             /* entry size in bytes */
    unsigned int count : 16;     /* count of items in listpack */
    unsigned int encoding : 2;   /* RAW==1 or LZF==2 */
    unsigned int container : 2;  /* PLAIN==1 or PACKED==2 */
    unsigned int recompress : 1; /* was this node previous compressed? */
    unsigned int attempted_compress : 1; /* node can't compress; too small */
    unsigned int dont_compress : 1; /* prevent compression of entry that will be used later */
    unsigned int extra : 9; /* more bits to steal for future usage */
} quicklistNode;

typedef struct quicklistEntry {
    const quicklist *quicklist;
    quicklistNode *node;
    unsigned char *zi; // ziplist指针
    unsigned char *value;
    long long longval;
    size_t sz;
    int offset; // ziplist的第几个节点
} quicklistEntry;

/* quicklistLZF is a 8+N byte struct holding 'sz' followed by 'compressed'.
 * 'sz' is byte length of 'compressed' field.
 * 'compressed' is LZF data with total (compressed) length 'sz'
 * NOTE: uncompressed length is stored in quicklistNode->sz.
 * When quicklistNode->entry is compressed, node->entry points to a quicklistLZF */
typedef struct quicklistLZF {
    size_t sz; /* LZF size in bytes*/
    char compressed[];
} quicklistLZF;

typedef struct quicklistIter {
    quicklist *quicklist;
    quicklistNode *current;
    unsigned char *zi; /* points to the current element */
    long offset; /* offset in current listpack */
    int direction;
} quicklistIter;
```
#### quicklistPush

```c
/* Wrapper to allow argument-based switching between HEAD/TAIL pop */
void quicklistPush(quicklist *quicklist, void *value, const size_t sz,
                   int where) {
    /* The head and tail should never be compressed (we don't attempt to decompress them) */
    if (quicklist->head)
        assert(quicklist->head->encoding != QUICKLIST_NODE_ENCODING_LZF);
    if (quicklist->tail)
        assert(quicklist->tail->encoding != QUICKLIST_NODE_ENCODING_LZF);

    if (where == QUICKLIST_HEAD) {
        quicklistPushHead(quicklist, value, sz);
    } else if (where == QUICKLIST_TAIL) {
        quicklistPushTail(quicklist, value, sz);
    }
}

/* Add new entry to head node of quicklist.
 *
 * Returns 0 if used existing head.
 * Returns 1 if new head created. */
int quicklistPushHead(quicklist *quicklist, void *value, size_t sz) {
    quicklistNode *orig_head = quicklist->head;
       
    /**
    __builtin_expect(expr, 0) 是 GCC 内置函数，含义是：“这个表达式大概率为 false”
    这能帮助编译器优化分支预测和 CPU 指令流水线，提高性能
    */   
    if (unlikely(isLargeElement(sz))) { // 判断如果是大对象，大对象>1G，直接作为明文插入，不压缩
        __quicklistInsertPlainNode(quicklist, quicklist->head, value, sz, 0);
        return 1;
    }

    if (likely(
            _quicklistNodeAllowInsert(quicklist->head, quicklist->fill, sz))) {
        quicklist->head->entry = lpPrepend(quicklist->head->entry, value, sz);
        quicklistNodeUpdateSz(quicklist->head);
    } else {
        quicklistNode *node = quicklistCreateNode();
        node->entry = lpPrepend(lpNew(0), value, sz);

        quicklistNodeUpdateSz(node);
        _quicklistInsertNodeBefore(quicklist, quicklist->head, node);
    }
    quicklist->count++;
    quicklist->head->count++;
    return (orig_head != quicklist->head);
}
```

#### 压缩与解压缩


### listpack

`listpack.h`,`listpack.c`

redis7之后，quickList中的ziplist替换成了listpack，并且redis打算使用listpack完全替代ziplist

其优势有以下几点：
1. 采用“线性块”设计，不再需要 prevlen，每个元素自包含，插入/删除不会引发级联修改
2. 写入操作时间复杂度更稳定。
3. 内存占用更低 
    - 整数压缩更极致：小整数（-64 到 127）用 1 个字节编码；
    - 字符串压缩优化：使用变长长度前缀（6/12/32bit）；
4. 更强的安全性
    - ziplist 曾被爆出构造漏洞（例如利用 prevlen 越界攻击）；
    - listpack 被设计为更健壮的结构，避免越界写、内存破坏；   
    - 更适合直接存储在 RDB/AOF 文件中。

#### listpack 总体结构

listpack 是一种连续内存块，结构如下：
```
+--------------------+
| Total Bytes (32b)  |  <-- 4 字节
+--------------------+
| Number of Elements |  <-- 2 字节
+--------------------+
| Entry 1            |
+--------------------+
| Entry 2            |
+--------------------+
| ...                |
+--------------------+
| Entry N            |
+--------------------+
| End Byte (0xFF)    |  <-- 1 字节
+--------------------+
```



| 字段名                  | 大小   | 说明                              |
| -------------------- | ---- | ------------------------------- |
| `Total Bytes`        | 4 字节 | 表示整个 listpack 的字节长度（包括结尾的 0xFF） |
| `Number of Elements` | 2 字节 | listpack 中的 entry 数量（实际元素个数）    |
| `Entries`            | 可变   | 由多个 entry（数据项）组成                |
| `End Byte`           | 1 字节 | 固定为 `0xFF`，表示 listpack 结尾       |


```c
#define LP_HDR_SIZE 6       /* 32 bit total len + 16 bit number of elements. */

#define LP_EOF 0xFF // 结尾标识符
```


```
[Header] + [Data] + [Backlen]
```

1. Encoding Header（变长）
前缀字节表示该 entry 的类型（整数/字符串）及其长度，规则如下：

| 前缀字节模式      | 类型          | 描述                                        |
| ----------- | ----------- | ----------------------------------------- |
| `0xxx xxxx` | `7BIT_UINT` | **7 位无符号整数**，数值直接编码在 header 的低 7 位，无需额外字节 |
| `10xx xxxx` | `6BIT_STR`  | **6 位字符串长度**，低 6 位表示字符串长度，后面跟字符串数据        |
| `110x xxxx` | `13BIT_INT` | **13 位整数**，与下一字节拼接，共 2 字节                 |
| `1110 xxxx` | `12BIT_STR` | **12 位字符串长度**，与下一字节拼接，最大支持 4095 字节字符串     |
| `1111 0000` | `32BIT_STR` | 后跟 4 字节表示字符串长度，再跟字符串内容                    |
| `1111 0001` | `16BIT_INT` | 后跟 2 字节有符号整数                              |
| `1111 0010` | `24BIT_INT` | 后跟 3 字节有符号整数                              |
| `1111 0011` | `32BIT_INT` | 后跟 4 字节有符号整数                              |
| `1111 0100` | `64BIT_INT` | 后跟 8 字节有符号整数                              |


2. Data就是数据部分

3. Backlen， 1-5个字节，这个存储了当前entry的总字节数量，方便从后向前遍历的时候能快速定位。这里有个非常精巧的设计，就是因为字节是变长，通过最高位是否为1，来确定是否继续读下一个字节。存储的时候也是高位字节在后，低位字节在前


#### lpNew
```c
/* Create a new, empty listpack.
 * On success the new listpack is returned, otherwise an error is returned.
 * Pre-allocate at least `capacity` bytes of memory,
 * over-allocated memory can be shrunk by `lpShrinkToFit`.
 * */
unsigned char *lpNew(size_t capacity) {
    unsigned char *lp = lp_malloc(capacity > LP_HDR_SIZE+1 ? capacity : LP_HDR_SIZE+1);
    if (lp == NULL) return NULL;
    lpSetTotalBytes(lp,LP_HDR_SIZE+1);// 设置所有的字节数量的字段
    lpSetNumElements(lp,0); // 设置一共有多少个元素
    lp[LP_HDR_SIZE] = LP_EOF; // 设置尾部
    return lp;
}
```
#### lpPrepend

#### lpInsert

#### lpFirst

#### lpDelete


### rax

前缀树
`rax.h`,`rax.c`

```c
typedef struct rax {
    raxNode *head;
    uint64_t numele;
    uint64_t numnodes;
} rax;


typedef struct raxNode {
    uint32_t iskey:1;     /* Does this node contain a key? */
    uint32_t isnull:1;    /* Associated value is NULL (don't store it). */
    uint32_t iscompr:1;   /* Node is compressed. */
    uint32_t size:29;     /* Number of children, or compressed string len. */
    /* Data layout is as follows:
     *
     * If node is not compressed we have 'size' bytes, one for each children
     * character, and 'size' raxNode pointers, point to each child node.
     * Note how the character is not stored in the children but in the
     * edge of the parents:
     *
     * [header iscompr=0][abc][a-ptr][b-ptr][c-ptr](value-ptr?)
     *
     * if node is compressed (iscompr bit is 1) the node has 1 children.
     * In that case the 'size' bytes of the string stored immediately at
     * the start of the data section, represent a sequence of successive
     * nodes linked one after the other, for which only the last one in
     * the sequence is actually represented as a node, and pointed to by
     * the current compressed node.
     *
     * [header iscompr=1][xyz][z-ptr](value-ptr?)
     *
     * Both compressed and not compressed nodes can represent a key
     * with associated data in the radix tree at any level (not just terminal
     * nodes).
     *
     * If the node has an associated key (iskey=1) and is not NULL
     * (isnull=0), then after the raxNode pointers pointing to the
     * children, an additional value pointer is present (as you can see
     * in the representation above as "value-ptr" field).
     */
    unsigned char data[];
} raxNode;


/* Stack data structure used by raxLowWalk() in order to, optionally, return
 * a list of parent nodes to the caller. The nodes do not have a "parent"
 * field for space concerns, so we use the auxiliary stack when needed. */
#define RAX_STACK_STATIC_ITEMS 32
typedef struct raxStack {
    void **stack; /* Points to static_items or an heap allocated array. */
    size_t items, maxitems; /* Number of items contained and total space. */
    /* Up to RAXSTACK_STACK_ITEMS items we avoid to allocate on the heap
     * and use this static array of pointers instead. */
    void *static_items[RAX_STACK_STATIC_ITEMS];
    int oom; /* True if pushing into this stack failed for OOM at some point. */
} raxStack;
```

### stream

`stream.h`,`t_stream.c`

### obj

`server.h`,`object.t`

```c
typedef struct redisObject {
    unsigned type:4;
    unsigned encoding:4;
    unsigned lru:LRU_BITS; /* LRU time (relative to global lru_clock) or
                            * LFU data (least significant 8 bits frequency
                            * and most significant 16 bits access time). */
    int refcount;
    void *ptr; // 指针
} robj;

/* Objects encoding. Some kind of objects like Strings and Hashes can be
 * internally represented in multiple ways. The 'encoding' field of the object
 * is set to one of this fields for this object. */
#define OBJ_ENCODING_RAW 0     /* Raw representation */
#define OBJ_ENCODING_INT 1     /* Encoded as integer */
#define OBJ_ENCODING_HT 2      /* Encoded as hash table */
#define OBJ_ENCODING_ZIPMAP 3  /* No longer used: old hash encoding. */
#define OBJ_ENCODING_LINKEDLIST 4 /* No longer used: old list encoding. */
#define OBJ_ENCODING_ZIPLIST 5 /* No longer used: old list/hash/zset encoding. */
#define OBJ_ENCODING_INTSET 6  /* Encoded as intset */
#define OBJ_ENCODING_SKIPLIST 7  /* Encoded as skiplist */
#define OBJ_ENCODING_EMBSTR 8  /* Embedded sds string encoding */
#define OBJ_ENCODING_QUICKLIST 9 /* Encoded as linked list of listpacks */
#define OBJ_ENCODING_STREAM 10 /* Encoded as a radix tree of listpacks */
#define OBJ_ENCODING_LISTPACK 11 /* Encoded as a listpack */


/* The actual Redis Object */
#define OBJ_STRING 0    /* String object. */
#define OBJ_LIST 1      /* List object. */
#define OBJ_SET 2       /* Set object. */
#define OBJ_ZSET 3      /* Sorted set object. */
#define OBJ_HASH 4      /* Hash object. */

/* The "module" object type is a special one that signals that the object
 * is one directly managed by a Redis module. In this case the value points
 * to a moduleValue struct, which contains the object value (which is only
 * handled by the module itself) and the RedisModuleType struct which lists
 * function pointers in order to serialize, deserialize, AOF-rewrite and
 * free the object.
 *
 * Inside the RDB file, module types are encoded as OBJ_MODULE followed
 * by a 64 bit module type ID, which has a 54 bits module-specific signature
 * in order to dispatch the loading to the right module, plus a 10 bits
 * encoding version. */
#define OBJ_MODULE 5    /* Module object. */
#define OBJ_STREAM 6    /* Stream object. */
```

#### cli命令实际执行的方法

`commands.c`文件中的变量`redisCommandTable`保存了所有命令的处理方法入口

```c
struct redisCommand redisCommandTable[] = { ...
```

处理请求命令的执行步骤:

processCommandAndResetClient(`networking.c`) --> processCommand(`server.c`) --> call(`server.c`) --> 
c->cmd->proc(c)(`server.c`)执行redisCommandTable中配置的方法


### redisDb

`db.c`

```c
/* Redis database representation. There are multiple databases identified
 * by integers from 0 (the default database) up to the max configured
 * database. The database number is the 'id' field in the structure. */
typedef struct redisDb {
    dict *dict;                 /* The keyspace for this DB */
    dict *expires;              /* Timeout of keys with a timeout set */
    dict *blocking_keys;        /* Keys with clients waiting for data (BLPOP)*/
    dict *ready_keys;           /* Blocked keys that received a PUSH */
    dict *watched_keys;         /* WATCHED keys for MULTI/EXEC CAS */
    int id;                     /* Database ID */
    long long avg_ttl;          /* Average TTL, just for stats */
    unsigned long expires_cursor; /* Cursor of the active expire cycle. */
    list *defrag_later;         /* List of key names to attempt to defrag one by one, gradually. */
    clusterSlotToKeyMapping *slots_to_keys; /* Array of slots to keys. Only used in cluster mode (db 0). */
} redisDb;
```

### redisServer

`server.h`

```c
struct redisServer {
    /* General */
    pid_t pid;                  /* Main process pid. */
    pthread_t main_thread_id;         /* Main thread id */
    char *configfile;           /* Absolute config file path, or NULL */
    char *executable;           /* Absolute executable file path. */
    char **exec_argv;           /* Executable argv vector (copy). */
    int dynamic_hz;             /* Change hz value depending on # of clients. */
    int config_hz;              /* Configured HZ value. May be different than
                                   the actual 'hz' field value if dynamic-hz
                                   is enabled. */
    mode_t umask;               /* The umask value of the process on startup */
    int hz;                     /* serverCron() calls frequency in hertz */
    int in_fork_child;          /* indication that this is a fork child */
    redisDb *db;
    dict *commands;             /* Command table */
    dict *orig_commands;        /* Command table before command renaming. */
    aeEventLoop *el;
    rax *errors;                /* Errors table */
    redisAtomic unsigned int lruclock; /* Clock for LRU eviction */
    volatile sig_atomic_t shutdown_asap; /* Shutdown ordered by signal handler. */
    mstime_t shutdown_mstime;   /* Timestamp to limit graceful shutdown. */
    int last_sig_received;      /* Indicates the last SIGNAL received, if any (e.g., SIGINT or SIGTERM). */
    int shutdown_flags;         /* Flags passed to prepareForShutdown(). */
    int activerehashing;        /* Incremental rehash in serverCron() */
    int active_defrag_running;  /* Active defragmentation running (holds current scan aggressiveness) */
    char *pidfile;              /* PID file path */
    int arch_bits;              /* 32 or 64 depending on sizeof(long) */
    int cronloops;              /* Number of times the cron function run */
    char runid[CONFIG_RUN_ID_SIZE+1];  /* ID always different at every exec. */
    int sentinel_mode;          /* True if this instance is a Sentinel. */
    size_t initial_memory_usage; /* Bytes used after initialization. */
    int always_show_logo;       /* Show logo even for non-stdout logging. */
    int in_exec;                /* Are we inside EXEC? */
    int busy_module_yield_flags;         /* Are we inside a busy module? (triggered by RM_Yield). see BUSY_MODULE_YIELD_ flags. */
    const char *busy_module_yield_reply; /* When non-null, we are inside RM_Yield. */
    int core_propagates;        /* Is the core (in oppose to the module subsystem) is in charge of calling propagatePendingCommands? */
    int propagate_no_multi;     /* True if propagatePendingCommands should avoid wrapping command in MULTI/EXEC */
    int module_ctx_nesting;     /* moduleCreateContext() nesting level */
    char *ignore_warnings;      /* Config: warnings that should be ignored. */
    int client_pause_in_transaction; /* Was a client pause executed during this Exec? */
    int thp_enabled;                 /* If true, THP is enabled. */
    size_t page_size;                /* The page size of OS. */
    /* Modules */
    dict *moduleapi;            /* Exported core APIs dictionary for modules. */
    dict *sharedapi;            /* Like moduleapi but containing the APIs that
                                   modules share with each other. */
    dict *module_configs_queue; /* Dict that stores module configurations from .conf file until after modules are loaded during startup or arguments to loadex. */
    list *loadmodule_queue;     /* List of modules to load at startup. */
    int module_pipe[2];         /* Pipe used to awake the event loop by module threads. */
    pid_t child_pid;            /* PID of current child */
    int child_type;             /* Type of current child */
    /* Networking */
    int port;                   /* TCP listening port */
    int tls_port;               /* TLS listening port */
    int tcp_backlog;            /* TCP listen() backlog */
    char *bindaddr[CONFIG_BINDADDR_MAX]; /* Addresses we should bind to */
    int bindaddr_count;         /* Number of addresses in server.bindaddr[] */
    char *bind_source_addr;     /* Source address to bind on for outgoing connections */
    char *unixsocket;           /* UNIX socket path */
    unsigned int unixsocketperm; /* UNIX socket permission (see mode_t) */
    socketFds ipfd;             /* TCP socket file descriptors */
    socketFds tlsfd;            /* TLS socket file descriptors */
    int sofd;                   /* Unix socket file descriptor */
    uint32_t socket_mark_id;    /* ID for listen socket marking */
    socketFds cfd;              /* Cluster bus listening socket */
    list *clients;              /* List of active clients */
    list *clients_to_close;     /* Clients to close asynchronously */
    list *clients_pending_write; /* There is to write or install handler. */
    list *clients_pending_read;  /* Client has pending read socket buffers. */
    list *slaves, *monitors;    /* List of slaves and MONITORs */
    client *current_client;     /* Current client executing the command. */

    /* Stuff for client mem eviction */
    clientMemUsageBucket* client_mem_usage_buckets;

    rax *clients_timeout_table; /* Radix tree for blocked clients timeouts. */
    long fixed_time_expire;     /* If > 0, expire keys against server.mstime. */
    int in_nested_call;         /* If > 0, in a nested call of a call */
    rax *clients_index;         /* Active clients dictionary by client ID. */
    pause_type client_pause_type;      /* True if clients are currently paused */
    list *postponed_clients;       /* List of postponed clients */
    mstime_t client_pause_end_time;    /* Time when we undo clients_paused */
    pause_event *client_pause_per_purpose[NUM_PAUSE_PURPOSES];
    char neterr[ANET_ERR_LEN];   /* Error buffer for anet.c */
    dict *migrate_cached_sockets;/* MIGRATE cached sockets */
    redisAtomic uint64_t next_client_id; /* Next client unique ID. Incremental. */
    int protected_mode;         /* Don't accept external connections. */
    int io_threads_num;         /* Number of IO threads to use. */
    int io_threads_do_reads;    /* Read and parse from IO threads? */
    int io_threads_active;      /* Is IO threads currently active? */
    long long events_processed_while_blocked; /* processEventsWhileBlocked() */
    int enable_protected_configs;    /* Enable the modification of protected configs, see PROTECTED_ACTION_ALLOWED_* */
    int enable_debug_cmd;            /* Enable DEBUG commands, see PROTECTED_ACTION_ALLOWED_* */
    int enable_module_cmd;           /* Enable MODULE commands, see PROTECTED_ACTION_ALLOWED_* */

    /* RDB / AOF loading information */
    volatile sig_atomic_t loading; /* We are loading data from disk if true */
    volatile sig_atomic_t async_loading; /* We are loading data without blocking the db being served */
    off_t loading_total_bytes;
    off_t loading_rdb_used_mem;
    off_t loading_loaded_bytes;
    time_t loading_start_time;
    off_t loading_process_events_interval_bytes;
    /* Fields used only for stats */
    time_t stat_starttime;          /* Server start time */
    long long stat_numcommands;     /* Number of processed commands */
    long long stat_numconnections;  /* Number of connections received */
    long long stat_expiredkeys;     /* Number of expired keys */
    double stat_expired_stale_perc; /* Percentage of keys probably expired */
    long long stat_expired_time_cap_reached_count; /* Early expire cycle stops.*/
    long long stat_expire_cycle_time_used; /* Cumulative microseconds used. */
    long long stat_evictedkeys;     /* Number of evicted keys (maxmemory) */
    long long stat_evictedclients;  /* Number of evicted clients */
    long long stat_total_eviction_exceeded_time;  /* Total time over the memory limit, unit us */
    monotime stat_last_eviction_exceeded_time;  /* Timestamp of current eviction start, unit us */
    long long stat_keyspace_hits;   /* Number of successful lookups of keys */
    long long stat_keyspace_misses; /* Number of failed lookups of keys */
    long long stat_active_defrag_hits;      /* number of allocations moved */
    long long stat_active_defrag_misses;    /* number of allocations scanned but not moved */
    long long stat_active_defrag_key_hits;  /* number of keys with moved allocations */
    long long stat_active_defrag_key_misses;/* number of keys scanned and not moved */
    long long stat_active_defrag_scanned;   /* number of dictEntries scanned */
    long long stat_total_active_defrag_time; /* Total time memory fragmentation over the limit, unit us */
    monotime stat_last_active_defrag_time; /* Timestamp of current active defrag start */
    size_t stat_peak_memory;        /* Max used memory record */
    long long stat_aof_rewrites;    /* number of aof file rewrites performed */
    long long stat_aofrw_consecutive_failures; /* The number of consecutive failures of aofrw */
    long long stat_rdb_saves;       /* number of rdb saves performed */
    long long stat_fork_time;       /* Time needed to perform latest fork() */
    double stat_fork_rate;          /* Fork rate in GB/sec. */
    long long stat_total_forks;     /* Total count of fork. */
    long long stat_rejected_conn;   /* Clients rejected because of maxclients */
    long long stat_sync_full;       /* Number of full resyncs with slaves. */
    long long stat_sync_partial_ok; /* Number of accepted PSYNC requests. */
    long long stat_sync_partial_err;/* Number of unaccepted PSYNC requests. */
    list *slowlog;                  /* SLOWLOG list of commands */
    long long slowlog_entry_id;     /* SLOWLOG current entry ID */
    long long slowlog_log_slower_than; /* SLOWLOG time limit (to get logged) */
    unsigned long slowlog_max_len;     /* SLOWLOG max number of items logged */
    struct malloc_stats cron_malloc_stats; /* sampled in serverCron(). */
    redisAtomic long long stat_net_input_bytes; /* Bytes read from network. */
    redisAtomic long long stat_net_output_bytes; /* Bytes written to network. */
    redisAtomic long long stat_net_repl_input_bytes; /* Bytes read during replication, added to stat_net_input_bytes in 'info'. */
    redisAtomic long long stat_net_repl_output_bytes; /* Bytes written during replication, added to stat_net_output_bytes in 'info'. */
    size_t stat_current_cow_peak;   /* Peak size of copy on write bytes. */
    size_t stat_current_cow_bytes;  /* Copy on write bytes while child is active. */
    monotime stat_current_cow_updated;  /* Last update time of stat_current_cow_bytes */
    size_t stat_current_save_keys_processed;  /* Processed keys while child is active. */
    size_t stat_current_save_keys_total;  /* Number of keys when child started. */
    size_t stat_rdb_cow_bytes;      /* Copy on write bytes during RDB saving. */
    size_t stat_aof_cow_bytes;      /* Copy on write bytes during AOF rewrite. */
    size_t stat_module_cow_bytes;   /* Copy on write bytes during module fork. */
    double stat_module_progress;   /* Module save progress. */
    size_t stat_clients_type_memory[CLIENT_TYPE_COUNT];/* Mem usage by type */
    size_t stat_cluster_links_memory; /* Mem usage by cluster links */
    long long stat_unexpected_error_replies; /* Number of unexpected (aof-loading, replica to master, etc.) error replies */
    long long stat_total_error_replies; /* Total number of issued error replies ( command + rejected errors ) */
    long long stat_dump_payload_sanitizations; /* Number deep dump payloads integrity validations. */
    long long stat_io_reads_processed; /* Number of read events processed by IO / Main threads */
    long long stat_io_writes_processed; /* Number of write events processed by IO / Main threads */
    redisAtomic long long stat_total_reads_processed; /* Total number of read events processed */
    redisAtomic long long stat_total_writes_processed; /* Total number of write events processed */
    /* The following two are used to track instantaneous metrics, like
     * number of operations per second, network traffic. */
    struct {
        long long last_sample_time; /* Timestamp of last sample in ms */
        long long last_sample_count;/* Count in last sample */
        long long samples[STATS_METRIC_SAMPLES];
        int idx;
    } inst_metric[STATS_METRIC_COUNT];
    long long stat_reply_buffer_shrinks; /* Total number of output buffer shrinks */
    long long stat_reply_buffer_expands; /* Total number of output buffer expands */

    /* Configuration */
    int verbosity;                  /* Loglevel in redis.conf */
    int maxidletime;                /* Client timeout in seconds */
    int tcpkeepalive;               /* Set SO_KEEPALIVE if non-zero. */
    int active_expire_enabled;      /* Can be disabled for testing purposes. */
    int active_expire_effort;       /* From 1 (default) to 10, active effort. */
    int active_defrag_enabled;
    int sanitize_dump_payload;      /* Enables deep sanitization for ziplist and listpack in RDB and RESTORE. */
    int skip_checksum_validation;   /* Disable checksum validation for RDB and RESTORE payload. */
    int jemalloc_bg_thread;         /* Enable jemalloc background thread */
    size_t active_defrag_ignore_bytes; /* minimum amount of fragmentation waste to start active defrag */
    int active_defrag_threshold_lower; /* minimum percentage of fragmentation to start active defrag */
    int active_defrag_threshold_upper; /* maximum percentage of fragmentation at which we use maximum effort */
    int active_defrag_cycle_min;       /* minimal effort for defrag in CPU percentage */
    int active_defrag_cycle_max;       /* maximal effort for defrag in CPU percentage */
    unsigned long active_defrag_max_scan_fields; /* maximum number of fields of set/hash/zset/list to process from within the main dict scan */
    size_t client_max_querybuf_len; /* Limit for client query buffer length */
    int dbnum;                      /* Total number of configured DBs */
    int supervised;                 /* 1 if supervised, 0 otherwise. */
    int supervised_mode;            /* See SUPERVISED_* */
    int daemonize;                  /* True if running as a daemon */
    int set_proc_title;             /* True if change proc title */
    char *proc_title_template;      /* Process title template format */
    clientBufferLimitsConfig client_obuf_limits[CLIENT_TYPE_OBUF_COUNT];
    int pause_cron;                 /* Don't run cron tasks (debug) */
    int latency_tracking_enabled;   /* 1 if extended latency tracking is enabled, 0 otherwise. */
    double *latency_tracking_info_percentiles; /* Extended latency tracking info output percentile list configuration. */
    int latency_tracking_info_percentiles_len;
    /* AOF persistence */
    int aof_enabled;                /* AOF configuration */
    int aof_state;                  /* AOF_(ON|OFF|WAIT_REWRITE) */
    int aof_fsync;                  /* Kind of fsync() policy */
    char *aof_filename;             /* Basename of the AOF file and manifest file */
    char *aof_dirname;              /* Name of the AOF directory */
    int aof_no_fsync_on_rewrite;    /* Don't fsync if a rewrite is in prog. */
    int aof_rewrite_perc;           /* Rewrite AOF if % growth is > M and... */
    off_t aof_rewrite_min_size;     /* the AOF file is at least N bytes. */
    off_t aof_rewrite_base_size;    /* AOF size on latest startup or rewrite. */
    off_t aof_current_size;         /* AOF current size (Including BASE + INCRs). */
    off_t aof_last_incr_size;       /* The size of the latest incr AOF. */
    off_t aof_last_incr_fsync_offset; /* AOF offset which is already requested to be synced to disk.
                                       * Compare with the aof_last_incr_size. */
    int aof_flush_sleep;            /* Micros to sleep before flush. (used by tests) */
    int aof_rewrite_scheduled;      /* Rewrite once BGSAVE terminates. */
    sds aof_buf;      /* AOF buffer, written before entering the event loop */
    int aof_fd;       /* File descriptor of currently selected AOF file */
    int aof_selected_db; /* Currently selected DB in AOF */
    time_t aof_flush_postponed_start; /* UNIX time of postponed AOF flush */
    time_t aof_last_fsync;            /* UNIX time of last fsync() */
    time_t aof_rewrite_time_last;   /* Time used by last AOF rewrite run. */
    time_t aof_rewrite_time_start;  /* Current AOF rewrite start time. */
    time_t aof_cur_timestamp;       /* Current record timestamp in AOF */
    int aof_timestamp_enabled;      /* Enable record timestamp in AOF */
    int aof_lastbgrewrite_status;   /* C_OK or C_ERR */
    unsigned long aof_delayed_fsync;  /* delayed AOF fsync() counter */
    int aof_rewrite_incremental_fsync;/* fsync incrementally while aof rewriting? */
    int rdb_save_incremental_fsync;   /* fsync incrementally while rdb saving? */
    int aof_last_write_status;      /* C_OK or C_ERR */
    int aof_last_write_errno;       /* Valid if aof write/fsync status is ERR */
    int aof_load_truncated;         /* Don't stop on unexpected AOF EOF. */
    int aof_use_rdb_preamble;       /* Specify base AOF to use RDB encoding on AOF rewrites. */
    redisAtomic int aof_bio_fsync_status; /* Status of AOF fsync in bio job. */
    redisAtomic int aof_bio_fsync_errno;  /* Errno of AOF fsync in bio job. */
    aofManifest *aof_manifest;       /* Used to track AOFs. */
    int aof_disable_auto_gc;         /* If disable automatically deleting HISTORY type AOFs?
                                        default no. (for testings). */

    /* RDB persistence */
    long long dirty;                /* Changes to DB from the last save */
    long long dirty_before_bgsave;  /* Used to restore dirty on failed BGSAVE */
    long long rdb_last_load_keys_expired;  /* number of expired keys when loading RDB */
    long long rdb_last_load_keys_loaded;   /* number of loaded keys when loading RDB */
    struct saveparam *saveparams;   /* Save points array for RDB */
    int saveparamslen;              /* Number of saving points */
    char *rdb_filename;             /* Name of RDB file */
    int rdb_compression;            /* Use compression in RDB? */
    int rdb_checksum;               /* Use RDB checksum? */
    int rdb_del_sync_files;         /* Remove RDB files used only for SYNC if
                                       the instance does not use persistence. */
    time_t lastsave;                /* Unix time of last successful save */
    time_t lastbgsave_try;          /* Unix time of last attempted bgsave */
    time_t rdb_save_time_last;      /* Time used by last RDB save run. */
    time_t rdb_save_time_start;     /* Current RDB save start time. */
    int rdb_bgsave_scheduled;       /* BGSAVE when possible if true. */
    int rdb_child_type;             /* Type of save by active child. */
    int lastbgsave_status;          /* C_OK or C_ERR */
    int stop_writes_on_bgsave_err;  /* Don't allow writes if can't BGSAVE */
    int rdb_pipe_read;              /* RDB pipe used to transfer the rdb data */
                                    /* to the parent process in diskless repl. */
    int rdb_child_exit_pipe;        /* Used by the diskless parent allow child exit. */
    connection **rdb_pipe_conns;    /* Connections which are currently the */
    int rdb_pipe_numconns;          /* target of diskless rdb fork child. */
    int rdb_pipe_numconns_writing;  /* Number of rdb conns with pending writes. */
    char *rdb_pipe_buff;            /* In diskless replication, this buffer holds data */
    int rdb_pipe_bufflen;           /* that was read from the rdb pipe. */
    int rdb_key_save_delay;         /* Delay in microseconds between keys while
                                     * writing the RDB. (for testings). negative
                                     * value means fractions of microseconds (on average). */
    int key_load_delay;             /* Delay in microseconds between keys while
                                     * loading aof or rdb. (for testings). negative
                                     * value means fractions of microseconds (on average). */
    /* Pipe and data structures for child -> parent info sharing. */
    int child_info_pipe[2];         /* Pipe used to write the child_info_data. */
    int child_info_nread;           /* Num of bytes of the last read from pipe */
    /* Propagation of commands in AOF / replication */
    redisOpArray also_propagate;    /* Additional command to propagate. */
    int replication_allowed;        /* Are we allowed to replicate? */
    /* Logging */
    char *logfile;                  /* Path of log file */
    int syslog_enabled;             /* Is syslog enabled? */
    char *syslog_ident;             /* Syslog ident */
    int syslog_facility;            /* Syslog facility */
    int crashlog_enabled;           /* Enable signal handler for crashlog.
                                     * disable for clean core dumps. */
    int memcheck_enabled;           /* Enable memory check on crash. */
    int use_exit_on_panic;          /* Use exit() on panic and assert rather than
                                     * abort(). useful for Valgrind. */
    /* Shutdown */
    int shutdown_timeout;           /* Graceful shutdown time limit in seconds. */
    int shutdown_on_sigint;         /* Shutdown flags configured for SIGINT. */
    int shutdown_on_sigterm;        /* Shutdown flags configured for SIGTERM. */

    /* Replication (master) */
    char replid[CONFIG_RUN_ID_SIZE+1];  /* My current replication ID. */
    char replid2[CONFIG_RUN_ID_SIZE+1]; /* replid inherited from master*/
    long long master_repl_offset;   /* My current replication offset */
    long long second_replid_offset; /* Accept offsets up to this for replid2. */
    int slaveseldb;                 /* Last SELECTed DB in replication output */
    int repl_ping_slave_period;     /* Master pings the slave every N seconds */
    replBacklog *repl_backlog;      /* Replication backlog for partial syncs */
    long long repl_backlog_size;    /* Backlog circular buffer size */
    time_t repl_backlog_time_limit; /* Time without slaves after the backlog
                                       gets released. */
    time_t repl_no_slaves_since;    /* We have no slaves since that time.
                                       Only valid if server.slaves len is 0. */
    int repl_min_slaves_to_write;   /* Min number of slaves to write. */
    int repl_min_slaves_max_lag;    /* Max lag of <count> slaves to write. */
    int repl_good_slaves_count;     /* Number of slaves with lag <= max_lag. */
    int repl_diskless_sync;         /* Master send RDB to slaves sockets directly. */
    int repl_diskless_load;         /* Slave parse RDB directly from the socket.
                                     * see REPL_DISKLESS_LOAD_* enum */
    int repl_diskless_sync_delay;   /* Delay to start a diskless repl BGSAVE. */
    int repl_diskless_sync_max_replicas;/* Max replicas for diskless repl BGSAVE
                                         * delay (start sooner if they all connect). */
    size_t repl_buffer_mem;         /* The memory of replication buffer. */
    list *repl_buffer_blocks;       /* Replication buffers blocks list
                                     * (serving replica clients and repl backlog) */
    /* Replication (slave) */
    char *masteruser;               /* AUTH with this user and masterauth with master */
    sds masterauth;                 /* AUTH with this password with master */
    char *masterhost;               /* Hostname of master */
    int masterport;                 /* Port of master */
    int repl_timeout;               /* Timeout after N seconds of master idle */
    client *master;     /* Client that is master for this slave */
    client *cached_master; /* Cached master to be reused for PSYNC. */
    int repl_syncio_timeout; /* Timeout for synchronous I/O calls */
    int repl_state;          /* Replication status if the instance is a slave */
    off_t repl_transfer_size; /* Size of RDB to read from master during sync. */
    off_t repl_transfer_read; /* Amount of RDB read from master during sync. */
    off_t repl_transfer_last_fsync_off; /* Offset when we fsync-ed last time. */
    connection *repl_transfer_s;     /* Slave -> Master SYNC connection */
    int repl_transfer_fd;    /* Slave -> Master SYNC temp file descriptor */
    char *repl_transfer_tmpfile; /* Slave-> master SYNC temp file name */
    time_t repl_transfer_lastio; /* Unix time of the latest read, for timeout */
    int repl_serve_stale_data; /* Serve stale data when link is down? */
    int repl_slave_ro;          /* Slave is read only? */
    int repl_slave_ignore_maxmemory;    /* If true slaves do not evict. */
    time_t repl_down_since; /* Unix time at which link with master went down */
    int repl_disable_tcp_nodelay;   /* Disable TCP_NODELAY after SYNC? */
    int slave_priority;             /* Reported in INFO and used by Sentinel. */
    int replica_announced;          /* If true, replica is announced by Sentinel */
    int slave_announce_port;        /* Give the master this listening port. */
    char *slave_announce_ip;        /* Give the master this ip address. */
    int propagation_error_behavior; /* Configures the behavior of the replica
                                     * when it receives an error on the replication stream */
    int repl_ignore_disk_write_error;   /* Configures whether replicas panic when unable to
                                         * persist writes to AOF. */
    /* The following two fields is where we store master PSYNC replid/offset
     * while the PSYNC is in progress. At the end we'll copy the fields into
     * the server->master client structure. */
    char master_replid[CONFIG_RUN_ID_SIZE+1];  /* Master PSYNC runid. */
    long long master_initial_offset;           /* Master PSYNC offset. */
    int repl_slave_lazy_flush;          /* Lazy FLUSHALL before loading DB? */
    /* Synchronous replication. */
    list *clients_waiting_acks;         /* Clients waiting in WAIT command. */
    int get_ack_from_slaves;            /* If true we send REPLCONF GETACK. */
    /* Limits */
    unsigned int maxclients;            /* Max number of simultaneous clients */
    unsigned long long maxmemory;   /* Max number of memory bytes to use */
    ssize_t maxmemory_clients;       /* Memory limit for total client buffers */
    int maxmemory_policy;           /* Policy for key eviction */
    int maxmemory_samples;          /* Precision of random sampling */
    int maxmemory_eviction_tenacity;/* Aggressiveness of eviction processing */
    int lfu_log_factor;             /* LFU logarithmic counter factor. */
    int lfu_decay_time;             /* LFU counter decay factor. */
    long long proto_max_bulk_len;   /* Protocol bulk length maximum size. */
    int oom_score_adj_values[CONFIG_OOM_COUNT];   /* Linux oom_score_adj configuration */
    int oom_score_adj;                            /* If true, oom_score_adj is managed */
    int disable_thp;                              /* If true, disable THP by syscall */
    /* Blocked clients */
    unsigned int blocked_clients;   /* # of clients executing a blocking cmd.*/
    unsigned int blocked_clients_by_type[BLOCKED_NUM];
    list *unblocked_clients; /* list of clients to unblock before next loop */
    list *ready_keys;        /* List of readyList structures for BLPOP & co */
    /* Client side caching. */
    unsigned int tracking_clients;  /* # of clients with tracking enabled.*/
    size_t tracking_table_max_keys; /* Max number of keys in tracking table. */
    list *tracking_pending_keys; /* tracking invalidation keys pending to flush */
    /* Sort parameters - qsort_r() is only available under BSD so we
     * have to take this state global, in order to pass it to sortCompare() */
    int sort_desc;
    int sort_alpha;
    int sort_bypattern;
    int sort_store;
    /* Zip structure config, see redis.conf for more information  */
    size_t hash_max_listpack_entries;
    size_t hash_max_listpack_value;
    size_t set_max_intset_entries;
    size_t zset_max_listpack_entries;
    size_t zset_max_listpack_value;
    size_t hll_sparse_max_bytes;
    size_t stream_node_max_bytes;
    long long stream_node_max_entries;
    /* List parameters */
    int list_max_listpack_size;
    int list_compress_depth;
    /* time cache */
    redisAtomic time_t unixtime; /* Unix time sampled every cron cycle. */
    time_t timezone;            /* Cached timezone. As set by tzset(). */
    int daylight_active;        /* Currently in daylight saving time. */
    mstime_t mstime;            /* 'unixtime' in milliseconds. */
    ustime_t ustime;            /* 'unixtime' in microseconds. */
    size_t blocking_op_nesting; /* Nesting level of blocking operation, used to reset blocked_last_cron. */
    long long blocked_last_cron; /* Indicate the mstime of the last time we did cron jobs from a blocking operation */
    /* Pubsub */
    dict *pubsub_channels;  /* Map channels to list of subscribed clients */
    dict *pubsub_patterns;  /* A dict of pubsub_patterns */
    int notify_keyspace_events; /* Events to propagate via Pub/Sub. This is an
                                   xor of NOTIFY_... flags. */
    dict *pubsubshard_channels;  /* Map shard channels to list of subscribed clients */
    /* Cluster */
    int cluster_enabled;      /* Is cluster enabled? */
    int cluster_port;         /* Set the cluster port for a node. */
    mstime_t cluster_node_timeout; /* Cluster node timeout. */
    char *cluster_configfile; /* Cluster auto-generated config file name. */
    struct clusterState *cluster;  /* State of the cluster */
    int cluster_migration_barrier; /* Cluster replicas migration barrier. */
    int cluster_allow_replica_migration; /* Automatic replica migrations to orphaned masters and from empty masters */
    int cluster_slave_validity_factor; /* Slave max data age for failover. */
    int cluster_require_full_coverage; /* If true, put the cluster down if
                                          there is at least an uncovered slot.*/
    int cluster_slave_no_failover;  /* Prevent slave from starting a failover
                                       if the master is in failure state. */
    char *cluster_announce_ip;  /* IP address to announce on cluster bus. */
    char *cluster_announce_hostname;  /* hostname to announce on cluster bus. */
    int cluster_preferred_endpoint_type; /* Use the announced hostname when available. */
    int cluster_announce_port;     /* base port to announce on cluster bus. */
    int cluster_announce_tls_port; /* TLS port to announce on cluster bus. */
    int cluster_announce_bus_port; /* bus port to announce on cluster bus. */
    int cluster_module_flags;      /* Set of flags that Redis modules are able
                                      to set in order to suppress certain
                                      native Redis Cluster features. Check the
                                      REDISMODULE_CLUSTER_FLAG_*. */
    int cluster_allow_reads_when_down; /* Are reads allowed when the cluster
                                        is down? */
    int cluster_config_file_lock_fd;   /* cluster config fd, will be flock */
    unsigned long long cluster_link_sendbuf_limit_bytes;  /* Memory usage limit on individual link send buffers*/
    int cluster_drop_packet_filter; /* Debug config that allows tactically
                                   * dropping packets of a specific type */
    /* Scripting */
    client *script_caller;       /* The client running script right now, or NULL */
    mstime_t busy_reply_threshold;  /* Script / module timeout in milliseconds */
    int pre_command_oom_state;         /* OOM before command (script?) was started */
    int script_disable_deny_script;    /* Allow running commands marked "no-script" inside a script. */
    /* Lazy free */
    int lazyfree_lazy_eviction;
    int lazyfree_lazy_expire;
    int lazyfree_lazy_server_del;
    int lazyfree_lazy_user_del;
    int lazyfree_lazy_user_flush;
    /* Latency monitor */
    long long latency_monitor_threshold;
    dict *latency_events;
    /* ACLs */
    char *acl_filename;           /* ACL Users file. NULL if not configured. */
    unsigned long acllog_max_len; /* Maximum length of the ACL LOG list. */
    sds requirepass;              /* Remember the cleartext password set with
                                     the old "requirepass" directive for
                                     backward compatibility with Redis <= 5. */
    int acl_pubsub_default;      /* Default ACL pub/sub channels flag */
    /* Assert & bug reporting */
    int watchdog_period;  /* Software watchdog period in ms. 0 = off */
    /* System hardware info */
    size_t system_memory_size;  /* Total memory in system as reported by OS */
    /* TLS Configuration */
    int tls_cluster;
    int tls_replication;
    int tls_auth_clients;
    redisTLSContextConfig tls_ctx_config;
    /* cpu affinity */
    char *server_cpulist; /* cpu affinity list of redis server main/io thread. */
    char *bio_cpulist; /* cpu affinity list of bio thread. */
    char *aof_rewrite_cpulist; /* cpu affinity list of aof rewrite process. */
    char *bgsave_cpulist; /* cpu affinity list of bgsave process. */
    /* Sentinel config */
    struct sentinelConfig *sentinel_config; /* sentinel config to load at startup time. */
    /* Coordinate failover info */
    mstime_t failover_end_time; /* Deadline for failover command. */
    int force_failover; /* If true then failover will be forced at the
                         * deadline, otherwise failover is aborted. */
    char *target_replica_host; /* Failover target host. If null during a
                                * failover then any replica can be used. */
    int target_replica_port; /* Failover target port */
    int failover_state; /* Failover state */
    int cluster_allow_pubsubshard_when_down; /* Is pubsubshard allowed when the cluster
                                                is down, doesn't affect pubsub global. */
    long reply_buffer_peak_reset_time; /* The amount of time (in milliseconds) to wait between reply buffer peak resets */
    int reply_buffer_resizing_enabled; /* Is reply buffer resizing enabled (1 by default) */
};
```


## key过期

官方文档中介绍
redis过期有两种方式
1.  a passive way
2.  an active way

passive way:
A key is passively expired simply when some client tries to access it, 
and the key is found to be timed out.

active way:
redis 有1秒10次的检验
1. test 20 random keys from set of keys with an associated expire
2. delete all the keys found expired
3. if more than 25% of keys were expired, start again from step 1.

## redis持久化

[官网对持久化的介绍](https://redis.io/topics/persistence)

作用： 用于redis的故障恢复

redis的持久化机制：
Redis provides a different range of persistence options:
1. RDB  进行时间点的数据库快照保存操作，周期性的dump内存数据到文件中

2. AOF  记录每次的写操作，redis重启的时候会进行回放，you can have different fsync policies: 
		no fsync at all, fsync every second, fsync at every query

3. 通过RDB或者AOF，都可以将redis内存中的数据给持久化到磁盘上去，然后可以将这些数据备份到别的地方去，比如可靠的云存储服务，如果redis服务器挂了，磁盘上的数据都丢了，可以从备份的云存储服务器上copy备份文件到新的redis服务器上去，恢复数据

4. 如果同时启用了RDB和AOF两种持久化机制，那么在redis重启的时候，会使用AOF来重新构建数据，因为AOF中的数据更加完整  


### RDB

#### 优点：
- RDB会生成多个数据文件，每个数据文件代表了某一个时刻中redis的数据，这种多个数据文件的方式，非常适合做冷备份，
可以将这种完整的数据文件发送到一些远程的安全存储上去，比如说Amazon的S3服务器，以预定好的备份策略来定期备份redis中的数据
    - AOF也可以做冷备份，可以周期性的copy AOF文件到备份服务器上去，但是需要自己写定时脚本处理
- RDB对redis对外提供的读写服务，影响非常小，可以让redis保持高性能，因为redis主进程只需要fork一个子进程执行磁盘IO操作来进行RDB持久化即可
    - RDB，每次写，都是直接写入redis内存中，只是在一定的时候，才会将数据写入磁盘
    - AOF，每次都是要写文件的，虽然可以快速写入os cache，但是还是有一定的时间开销的，速度肯定比RDB略慢一些
- 相对于AOF来说，直接基于RDB数据文件来重启和恢复redis数据，更加快速
    - AOF，存放的是指令日志，做数据恢复的时候，要回放所有的指令
    - RDB，就是一份数据文件，恢复的时候，直接加载到内存中即可

综上所述，RDB特别适合做冷备份

#### 缺点：
- 如果想要在redis故障时，尽可能少的丢失数据，那么RDB没有AOF好，一般RDB的快照周期是5分钟，或者更长时间一次，这个时候得接受一旦redis进程宕机，那么会丢失最近5分钟的数据
    - 这个问题是RDB最大的缺点，不适合做第一优先的恢复方案
- RDB诶次在fork子进程来执行RDB快照数据文件生成的时候，如果数据文件特别大，可能会导致对客户端提供的服务暂停数毫秒，或者甚至数秒


#### 如何配置

redis.conf文件中，  
`save 60 10000`  
每超过60s，如果有超过10000个key发生了变更，那么就生成一个新的dump.rdb文件，就是当前redis内存中完整的数据,
这个操作也被称之为snapshotting,

也可以手动调用`save`或者`bsave` 来同步或者异步的生成快照


#### 工作流程

1. redis根据配置的检查点，尝试去生成rdb快照文件
2. fork一个子进程出来
3. 子进程尝试将数据dump到临时的rdb快照文件中
4. 完成rdb快照文件的生成之后，就替换之前的旧的快照文件
5. 如果通过`redis-cli shutdown`的方式，关掉redis，会立即生成一份rdb快照


#### 源码

`rdb.c`

##### 触发方式
- rdbSaveBackground --> rdbSave --> rdbSaveRio --> rdbSaveDb

##### COW（Copy On Write）

- COW：写时复制  linux的fork
- 父子进程有自己的虚拟内存但共享物理内存
- 数据段页面分离
- 数据改变时，kernel复制改变的数据页
- 子进程的数据在fork的那一刻的固定了


### AOF

#### 优点：

- AOF可以更好的保护数据不丢失，一般AOF会每隔1秒，通过一个后台线程执行一次fsync操作，最多丢失1秒钟的数据
- AOF日志文件是用append-only的模式写入的，没有任何磁盘寻址的开销，性能非常高，而且文件不易破损，即使文件尾部损坏，也很容易修复
- AOF日志文件即使过大的时候，出现后台重写操作，也不会影响客户端的读写，因为在rewrite log的时候，会对其中指令进行压缩，创建出一份需要恢复数据的最小日志出来，再创建新日志文件的时候，老的日志文件还是照常写入，当新的merge后的日志文件ready的时候，再交换新老日志文件即可，
- AOF日志文件的命令通过人类可读的方式进行记录，这个特性非常适合做灾难性的误删除的紧急恢复，比如某人不小心用flushall命令清空了所有数据，只要这个时候后台rewrite还没有发生，那么就可以立即copy AOF文件，将最后一条flushall命令给删了，然后再将该AOF文件放回去，就可以通过恢复机制，自动恢复所有数据

#### 缺点：

- 对于同一份数据来说，AOF日志文件通常比RDB数据快照文件要大
- AOF开启后，支持的写QPS会比RDB支持的写QPS低，因为AOF一般会配置成每秒fsync一次日志文件记录，当然，每秒一次fsync，性能还是很高的
    - 如果你要保证一条数据都不丢，也是可以的，AOF的fsync设置成每写入一条数据，fsync一次，那就完蛋了，redis的QPS会大大降低
- 以前AOF发生过BUG，就是通过AOF记录的日志，进行数据恢复的时候，没有恢复一模一样的数据出来，所以说，类似AOF这种缴费负载的基于命令日志/merge/回放的方式，比基于RDB每次持久化一份完整的数据快照文件的方式，更加脆弱一些，容易有bug，不过AOF就是为了避免rewrite过程导致的bug,因此每次rewrite并不是基于旧的指令日志进行merge的，而是基于当前内存中的数据进行指令的重新构建，这样健壮性会好很多

- 做数据恢复的时候比较慢，如果做冷备份的话，定期脚本要自己写


#### 如何配置

AOF持久化，默认是关闭的
`redis.conf`中`appendonly yes`配置后就可以打开了。在生产环境中，一般来说AOF都是要打开的，
即使AOF和RDB都打开了，redis重启的时候，也是优先通过AOF进行数据的恢复

可以配置AOF的fsync的策略
- `appendfsync always`  每次写入一条数据，立即将这个数据对应的写日志fsync到磁盘上去，新能非常差
- `appendfsync everysec` 每秒执行fsync操作，生产环境一般这样配置，性能很高
- `appendfsync no` redis仅仅将数据写入到`os cache`就不管了

#### 配置 AOF rewrite

redis的内存有限，很多数据可能会自动过期，可能会被用户删除，也可能会被redis用缓存清楚的算法清理掉

```conf
# Automatic rewrite of the append only file.
# Redis is able to automatically rewrite the log file implicitly calling
# BGREWRITEAOF when the AOF log size grows by the specified percentage.
#
# This is how it works: Redis remembers the size of the AOF file after the
# latest rewrite (if no rewrite has happened since the restart, the size of
# the AOF at startup is used).
#
# This base size is compared to the current size. If the current size is
# bigger than the specified percentage, the rewrite is triggered. Also
# you need to specify a minimal size for the AOF file to be rewritten, this
# is useful to avoid rewriting the AOF file even if the percentage increase
# is reached but it is still pretty small.
#
# Specify a percentage of zero in order to disable the automatic AOF
# rewrite feature.
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

#### AOF Rewrite流程

1. redis fork一个子进程
2. 子进程是基于当前内存中的数据，构建日志，开始往一个新的临时的AOF文件中写入日志
3. redis主进程在内存中写入日志，同时新的日志也继续写入旧的AOF文件
4. 子进程写完了之后，主进程将内存中的新日志再次追加到新的AOF文件中
5. 用新的日志文件替换掉旧的日志文件


#### AOF文件破损修复

如果redis在append数据到文件中时，机器宕机了，可能会导致AOF文件破损

可以使用 `redis-check-aof --fix` 命令来修复破损的AOF文件

#### AOF和RDB同时工作

1. 如果RDB在执行snapshotting的过程中，redis不会执行AOF rewrite操作，如果在执行AOF rewrite操作过程中，则不会执行RDB snapshotting
2. 如果RDB在执行snapshotting的过程中，用户手动执行了 `BGREWRITEAOF` 命令，要等RDB 快照生成后，才会执行
3. 同时有RDB和AOF的持久化文件，那么redis重启的时候，会优先使用AOF进行数据恢复，因为其中的日志更完整


#### 源码

`aof.c`


call(`server.c`) --> afterCommand(`server.c`) --> propagatePendingCommands(`server.c`) --> propagateNow(`server.c`) --> feedAppendOnlyFile(`aof.c`) --> `server.aof_buf` 

--> 定时 --> flushAppendOnlyFile(`aof.c`) --> aofWrite(`aof.c`) --> 写入到文件



### RDB和AOF该如何选择

- 不要仅仅使用RDB，因为那样会导致你丢失很多的数据
- 也不要仅仅使用AOF，因为那样有两个问题
    1.  你通过AOF做冷备份，没有RDB冷备份，来的恢复速度快
    2.  RDB每次简单粗暴生成快照数据，更加健壮，可以避免AOF这种复杂的备份和恢复机制的bug
- 综合使用AOF和RDB两种持久化机制，用AOF来保证数据不丢失，作为数据恢复的一种选择，用RDB来做不同程度的冷备份，在AOF文件都丢失或损坏的情况下，还可以使用RDB来进行快速的数据恢复 



### redis企业级配置方案

#### 企业级持久化配置策略

1. RDB的生成策略用默认的就差不多
2. AOF一定要打开， `fsync everysec`
3. 适当调整下面两个配置，用默认的也是可以的
```conf
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

#### 数据备份方案

1. 写crontab定时调度脚本去做数据备份
2. 每小时都copy一份rdb的备份，到一个目录中去，仅仅保留最近48小时的备份
3. 每天都保留一份当日的RDB的备份，到一个目录中去，仅仅保留最近一个月的备份
4. 每次copy备份的时候，都把太旧的备份给删了
5. 每天晚上将当前服务器上所有的数据备份，发送一份到远程的云服务器上去

##### 每小时copy一次备份，删除48小时前的数据
``` shell
crontab -e

0 * * * * sh /usr/local/redis/copy/redis_rdb_copy_hourly.sh
```

redis_rdb_copy_hourly.sh

```shell
#!/bin/sh 

cur_date=`date +%Y%m%d%k`
rm -rf /usr/local/redis/snapshotting/$cur_date
mkdir /usr/local/redis/snapshotting/$cur_date
cp /var/redis/6379/dump.rdb /usr/local/redis/snapshotting/$cur_date

del_date=`date -d -48hour +%Y%m%d%k`
rm -rf /usr/local/redis/snapshotting/$del_date
```

##### 每天copy一次备份

```shell
crontab -e

0 0 * * * sh /usr/local/redis/copy/redis_rdb_copy_daily.sh
```

redis_rdb_copy_daily.sh

```shell
#!/bin/sh 

cur_date=`date +%Y%m%d`
rm -rf /usr/local/redis/snapshotting/$cur_date
mkdir /usr/local/redis/snapshotting/$cur_date
cp /var/redis/6379/dump.rdb /usr/local/redis/snapshotting/$cur_date

del_date=`date -d -1month +%Y%m%d`
rm -rf /usr/local/redis/snapshotting/$del_date
```

#####  每天一次将所有数据上传一次到远程的云服务器上去

#### 数据恢复方案

1. 如果是redis进程挂掉，那么重启redis进程即可，直接基于AOF日志文件恢复数据
2. 如果是redis进程所在机器挂掉，那么重启机器后，尝试重启redis进程，尝试直接基于AOF日志文件进行数据恢复
3. 如果redis当前最新的AOF和RDB文件出现了丢失/损坏，那么可以尝试基于该机器上当前的某个最新的RDB数据副本进行数据恢复
    1. 停止redis
    2. 配置文件关闭AOF
    3. 拷贝rdb备份 
    4. 重启redis 
    5. 确认数据恢复
    6. 在命令行热修改redis配置，打开AOF，这个时候redis会将内存中的数据对应的日志，写入AOF文件中去
    7. 停止redis
    8. 修改配置文件，打开AOF
    9. 再次重启AOF
4. 如果当前机器上的所有RDB文件全部损坏，那么从远程的云服务上拉取最新的RDB快照回来恢复数据
5. 如果是发现有重大的数据错误，比如某个小时上线的程序一下子将数据全部污染了，数据全错了，那么可以选择某个更早的时间点，对数据进行恢复
   - 举个例子，12点上线了代码，发现代码有bug，导致代码生成的所有的缓存数据，写入redis，全部错了
     找到一份11点的rdb的冷备，然后按照上面的步骤，去恢复到11点的数据，不就可以了吗






## Redis主从架构+读写分离

redis replication -> 主从架构 -> 读写分离 -> 水平扩容支撑读高并发

### redis replication

#### 核心机制
[官方文档](https://redis.io/topics/replication) 

1. redis采用异步方式复制数据到slave节点，不过redis 2.8开始，slave node会周期性地确认自己每次复制的数据量
2. 一个master node是可以配置多个slave node的
3. slave node也可以连接其他的slave node
4. slave node做复制的时候，是不会block master node的正常工作的
5. slave node在做复制的时候，也不会block对自己的查询操作，它会用旧的数据集来提供服务; 但是复制完成的时候，需要删除旧数据集，加载新数据集，这个时候就会暂停对外服务了
6. slave node主要用来进行横向扩容，做读写分离，扩容的slave node可以提高读的吞吐量

#### 核心原理

当启动一个slave node的时候，它会发送一个PSYNC命令给master node

如果这是slave node重新连接master node，那么master node仅仅会复制给slave部分缺少的数据; 否则如果是slave node第一次连接master node，那么会触发一次full resynchronization

开始full resynchronization的时候，master会启动一个后台线程，开始生成一份RDB快照文件，同时还会将从客户端收到的所有写命令缓存在内存中。RDB文件生成完毕之后，master会将这个RDB发送给slave，slave会先写入本地磁盘，然后再从本地磁盘加载到内存中。然后master会将内存中缓存的写命令发送给slave，slave也会同步这些数据。

slave node如果跟master node有网络故障，断开了连接，会自动重连。master如果发现有多个slave node都来重新连接，仅仅会启动一个rdb save操作，用一份数据服务所有slave node。

#### 主从复制的断点续传

从redis 2.8开始，就支持主从复制的断点续传，如果主从复制过程中，网络连接断掉了，那么可以接着上次复制的地方，继续复制下去，而不是从头开始复制一份

master node会在内存中常见一个backlog，master和slave都会保存一个replica offset还有一个master id，offset就是保存在backlog中的。如果master和slave网络连接断掉了，slave会让master从上次的replica offset开始继续复制

但是如果没有找到对应的offset，那么就会执行一次resynchronization

#### 无磁盘化复制

master在内存中直接创建rdb，然后发送给slave，不会在自己本地落地磁盘了

repl-diskless-sync
repl-diskless-sync-delay，等待一定时长再开始复制，因为要等更多slave重新连接过来

#### 过期key处理

slave不会过期key，只会等待master过期key。如果master过期了一个key，或者通过LRU淘汰了一个key，那么会模拟一条del命令发送给slave。


#### 安装redis集群

#### Docker安装

1. 配置Master redis.conf文件

创建目录
```shell
mkdir -p /home/poul/workspace/soft/docker/redis-01/data
## 复制一份默认的redis配置文件到 /home/poul/workspace/soft/docker/redis-01 下
```

修改Master redis.conf配置

```conf
## 修改bind地址
bind 0.0.0.0 -::1
## RDB配置
save 3600 1
save 300 100
save 60 10000

## 打开AOF
appendonly yes
appendfsync everysec
## 持久化目录
dir /data
## 安全认证
masterauth redis-pass
requirepass redis-pass
```

2. 启动Master Docker镜像 将目录 `/usr/local/etc/redis/` 映射到到宿主机的目录方便操作

```shell
## 先用`--rm`参数测试 不要加`-d` 
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-01:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-01/data:/data -p 6379:6379 --name redis-01 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 测试通过后再加上`-d` 参数，并去掉 `--rm`参数
sudo docker run  -v /home/poul/workspace/soft/docker/redis-01:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-01/data:/data -p 6379:6379 --name redis-01 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

3. 配置Slave `redis.conf`文件

```shell
mkdir -p /home/poul/workspace/soft/docker/redis-02/data
## 复制一份默认的redis配置文件到 /home/poul/workspace/soft/docker/redis-01 下

## 查询一下主节点的ip 给下面的配置使用
sudo docker inspect redis-01 | grep IPAddres
```

修改Slave redis.conf配置

```conf
## 修改bind地址
bind 0.0.0.0 -::1
## RDB配置
save 3600 1
save 300 100
save 60 10000

## 打开AOF
appendonly yes
appendfsync everysec
## 持久化目录
dir /data
## 安全认证
masterauth redis-pass
requirepass redis-pass

## 配置master机器
replicaof 172.17.0.2 6379

## 从节点设置为制度
replica-read-only yes
```


4. 启动Slave Docker镜像 将目录 `/usr/local/etc/redis/` 映射到到宿主机的目录方便操作

```shell
## 先用`--rm`参数测试 不要加`-d` 
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-02:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-02/data:/data -p 6479:6379 --name redis-02 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 测试通过后再加上`-d` 参数，并去掉 `--rm`参数
sudo docker run -v /home/poul/workspace/soft/docker/redis-02:/usr/local/etc/redis  -v /home/poul/workspace/soft/docker/redis-02/data:/data -p 6479:6379 --name redis-02 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

5. 在redis命令行里可以通过执行 `info replication` 命令 查看节点的复制状态 



### redis主从架构下如果做到99.99%高可用

如果你的系统可以保证在全年，99.99%的时间内，都是处于可用的状态的，那么就可以称之为高可用性

redis主从架构下有个问题，就是master节点，一点挂掉后，整个集群就不可以用了，以此，引出了，一个概念，sentinel/sentry 哨兵模式

#### 哨兵

[官方文档](https://redis.io/topics/sentinel '')

哨兵是redis集群架构中非常重要的一个组件,主要功能如下
1. 集群监控 负责监控redis master 和 slave进程是否正常工作
2. 消息通知 如果某个redis 实例有故障，那么哨兵负责发送消息作为报警通知给管理员
3. 故障转移(failover) 如果master node挂掉了，会自动转移到slave node上
4. 配置中心， 如果故障转移发生了，通知client客户端新的master地址


哨兵本身也是分布式的，作为一个哨兵集群去运行，互相协同工作
1. 故障转移时，判断一个master node是否宕机了，需要大部分的哨兵都同意才行，涉及到了分布式选举的问题
2. 即使部分哨兵节点挂掉了，哨兵集群还是能正常工作的，因为如果一个作为高可用机制重要组成部分的故障转移系统本身就是单点的，那就很坑了


哨兵的核心知识
1. 哨兵至少需要3个实例，来保证自己的健壮性
2. 哨兵+redis主从的部署架构，是不会保证数据零丢失的，只能保证redis集群的高可用性
3. 对于哨兵 + redis主从这种复杂的部署架构，尽量在测试环境和生产环境，都进行充足的测试和演练


为什么哨兵集群只有两个节点无法正常工作，哨兵集群必须部署2个以上节点？

如果哨兵集群仅仅部署了个2个哨兵实例，quorum=1

```
+----+         +----+
| M1 |---------| R1 |
| S1 |         | S2 |
+----+         +----+
```
Configuration: quorum = 1

master宕机，s1和s2中只要有1个哨兵认为master宕机就可以还行切换，同时s1和s2中会选举出一个哨兵来执行故障转移
同时这个时候，需要majority，也就是大多数哨兵都是运行的，2个哨兵的majority就是2（2的majority=2，3的majority=2，5的majority=3，4的majority=2），2个哨兵都运行着，就可以允许执行故障转移
但是如果整个M1和S1运行的机器宕机了，那么哨兵只有1个了，此时就没有majority来允许执行故障转移，虽然另外一台机器还有一个R1，但是故障转移不会执行

经典的3节点哨兵集群

```
       +----+
       | M1 |
       | S1 |
       +----+
          |
+----+    |    +----+
| R2 |----+----| R3 |
| S2 |         | S3 |
+----+         +----+
```
Configuration: quorum = 2，majority
如果M1所在机器宕机了，那么三个哨兵还剩下2个，S2和S3可以一致认为master宕机，然后选举出一个来执行故障转移
同时3个哨兵的majority是2，所以还剩下的2个哨兵运行着，就可以允许执行故障转移

#### 哨兵的安装
##### Docker下安装

复制一份默认的sentinel.conf文件到目录 `/home/poul/workspace/soft/docker/redis-sentinel-01`

修改sentinel的配置文件如下:
```conf
## 配置工作目录
dir /data

## 监听的master结点
sentinel monitor mymaster 172.17.0.2  6379 2

sentinel down-after-milliseconds mymaster 30000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

## master节点的密码
sentinel auth-pass mymaster redis-pass
```

```shell
## 先测试
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-01:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-01/data:/data -p 26379:26379 --name redis-sentinel-01 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

## ok后直接后台启动
sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-01:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-01/data:/data -p 26379:26379 --name redis-sentinel-01 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

## 其他两个节点如法炮制
sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-02:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-02/data:/data -p 26479:26379 --name redis-sentinel-02 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-02:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-02/data:/data -p 26479:26379 --name redis-sentinel-02 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf


sudo docker run --rm -v /home/poul/workspace/soft/docker/redis-sentinel-03:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-03/data:/data -p 26579:26379 --name redis-sentinel-03 redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf

sudo docker run -it -v /home/poul/workspace/soft/docker/redis-sentinel-03:/usr/local/etc/redis -v /home/poul/workspace/soft/docker/redis-sentinel-03/data:/data -p 26579:26379 --name redis-sentinel-03 -d redis:6.2.5 redis-sentinel /usr/local/etc/redis/sentinel.conf
```

连到某个哨兵上查询信息 

```shell
redis-cli -p 26379
```

```shell
sentinel master mymaster
```


### redis cluster

#### 原理

多master + 读写分离 + 高可用

- [Redis Cluster tutorial](https://redis.io/topics/cluster-tutorial): a gentle introduction and setup guide to Redis Cluster.
- [Redis Cluster specification](https://redis.io/topics/cluster-spec): the more formal description of the behavior and algorithms used in Redis Cluster.

1. 自动将数据进行分片，每个master上放一部分数据
2. 提供内置的高可用支持，部分master不可用时，还是可以继续工作的

在redis cluster架构下，每个redis要放开两个端口号，比如一个是6379，另外一个就是加10000的端口号，比如16379  
16379端口号是用来进行节点间通信的，也就是cluster bus的东西，集群总线。cluster bus的通信，用来进行故障检测，配置更新，故障转移授权  
cluster bus用了另外一种二进制的协议，主要用于节点间进行高效的数据交换，占用更少的网络带宽和处理时间

至少3个master节点启动，官方建议每个master带一个slave，这样就是6台机器

分布式数据存储的核心算法  
hash算法 -> 一致性hash算法（memcached） -> redis cluster，hash slot算法

1. 最老土的hash算法和弊端（大量缓存重建）
2. 一致性hash算法（自动缓存迁移）+虚拟节点（自动负载均衡）
3. redis cluster的hash slot算法  
    redis cluster有固定的16384个hash slot，对每个key计算CRC16值，然后对16384取模，可以获取key对应的hash slot  
    redis cluster中每个master都会持有部分slot，比如有3个master，那么可能每个master持有5000多个hash slot  
    hash slot让node的增加和移除很简单，增加一个master，就将其他master的hash slot移动部分过去，减少一个master，就将它的hash slot移动到其他master上去  
    移动hash slot的成本是非常低的  
    客户端的api，可以对指定的数据，让他们走同一个hash slot，通过hash tag来实现  



#### 安装Redis Cluster

##### Docker中安装

1. 配置redis.conf文件

```conf
bind 0.0.0.0
port 7001
cluster-enabled yes
cluster-config-file /data/7001.conf
cluster-node-timeout 15000
daemonize	yes	

pidfile		/var/run/redis_7001.pid 						
dir 		/data	
appendonly yes

## 安全认证
masterauth redis-pass
requirepass redis-pass
```

2. 启动docker container

```shell
# 创建一个给redis-cluster使用的网络
sudo docker network create redis-cluster

# 尝试启动一下
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-01/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-01/data:/data -p 7001:7001 --name redis-cluster-01 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-01/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-01/data:/data -p 7001:7001 --name redis-cluster-01 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 其他5个节点 如法炮制
## 02
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-02/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-02/data:/data -p 7002:7001 --name redis-cluster-02 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-02/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-02/data:/data -p 7002:7001 --name redis-cluster-02 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 03
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-03/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-03/data:/data -p 7003:7001 --name redis-cluster-03 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-03/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-03/data:/data -p 7003:7001 --name redis-cluster-03 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

## 04 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-04/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-04/data:/data -p 7004:7001 --name redis-cluster-04 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-04/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-04/data:/data -p 7004:7001 --name redis-cluster-04 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 05 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-05/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-05/data:/data -p 7005:7001 --name redis-cluster-05 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-05/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-05/data:/data -p 7005:7001 --name redis-cluster-05 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 06
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-06/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-06/data:/data -p 7006:7001 --name redis-cluster-06 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-06/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-06/data:/data -p 7006:7001 --name redis-cluster-06 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
# 后台启动
```

3. 创建集群

`gem install redis`

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster create 172.18.0.2:7001 172.18.0.3:7001 172.18.0.4:7001 172.18.0.5:7001  172.18.0.6:7001  172.18.0.7:7001 --cluster-replicas 1 -a redis-pass
```

校验一下  

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster check 172.17.0.2:7001 -a redis-pass
```

**注意：** 
1. 在slave节点上查询操作，第一次建立连接时 需要执行一下 `readonly` 命令
2. 通过 `./redis-cli -c` 可以自动重定向到key所在的节点
3. 读写分离的redis-cluster，的java客户端实现问题   
    如果你要让最流行的jedis做redis cluster的读写分离的访问，那可能还得自己修改一点jedis的源码，成本比较高  
    要不然你就是自己基于jedis，封装一下，自己做一个redis cluster的读写分离的访问api  
    核心的思路，就是说，redis cluster的时候，就没有所谓的读写分离的概念了  
    读写分离，是为了什么，主要是因为要建立一主多从的架构，才能横向任意扩展slave node去支撑更大的读吞吐量  
    redis cluster的架构下，实际上本身master就是可以任意扩展的，你如果要支撑更大的读吞吐量，或者写吞吐 量，或者数据量，都可以直接对master进行横向扩展就可以了?? 但是某个master挂了数据不久丢了吗  

4. 压测一下试试

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-benchmark -p 7001 --cluster -a redis-pass --csv
```

5. 手动扩容redis集群

```conf
## 07 
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-07/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-07/data:/data -p 7007:7001 --name redis-cluster-07 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-07/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-07/data:/data -p 7007:7001 --name redis-cluster-07 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
## 08
sudo docker run --network redis-cluster --rm -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-08/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-08/data:/data -p 7008:7001 --name redis-cluster-08 redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf

sudo docker run --network redis-cluster -it -v /etc/localtime:/etc/localtime -v /home/poul/workspace/soft/docker/redis-cluster-08/:/usr/local/etc/redis/ -v /home/poul/workspace/soft/docker/redis-cluster-08/data:/data -p 7008:7001 --name redis-cluster-08 -d redis:6.2.5 redis-server /usr/local/etc/redis/redis.conf
```

执行命令

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster add-node 172.17.0.8:7001 172.17.0.2:7001 -a redis-pass

/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster add-node 172.17.0.9:7001 172.17.0.2:7001 -a redis-pass --cluster-slave --cluster-master-id 98c710d43e7ff7f9a035cdba511d621ec0bbd423
```

6. reshard 

```shell
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster reshard 172.17.0.2:7001 -a redis-pass

## 然后根据下面的提示一步一步操作
## 会提示要移动多少slots 这个地方用公式 (2 ^ 14 / master数量 ) 得到这个数就可以了
How many slots do you want to move (from 1 to 16384)?

## 输入要接受 新的slot的节点id 
What is the receiving node ID?

## 输入 想从哪些节点 move slot 可输入多个 输入完成后 再输入done 结束
Please enter all the source node IDs.
  Type 'all' to use all the nodes as source nodes for the hash slots.
  Type 'done' once you entered all the source nodes IDs.
  Source node #1:

## 是否接受 reshard plan，接受的话 输入yes 
Do you want to proceed with the proposed reshard plan (yes/no)? 
```

删除node

```shell
## 如果被删除的节点的slot非空的话需要先把结点中的slot平均move到其他节点 需要移动的slot数目为 被移除节点slot / 剩余master节点数量 ，然后一个一个的移动
/home/poul/workspace/soft/redis/redis6/bin/redis-cli --cluster del-node 127.0.0.2:7001 54478f516721e01586322939a5044169abc670f7 -a redis-pass
```

#### Slave的自动迁移
比如现在有10个master，每个有1个slave，然后新增了3个slave作为冗余，有的master就有2个slave了，有的master出现了salve冗余  
如果某个master的slave挂了，那么redis cluster会自动迁移一个冗余的slave给那个master  
只要多加一些冗余的slave就可以了  
为了避免的场景，就是说，如果你每个master只有一个slave，万一说一个slave死了，然后很快，master也死了，那可用性还是降低了  
但是如果你给整个集群挂载了一些冗余slave，那么某个master的slave死了，冗余的slave会被自动迁移过去，作为master的新slave，此时即使那个master也死了  
还是有一个slave会切换成master的  
之前有一个master是有冗余slave的，直接让其他master其中的一个slave死掉，然后看有冗余slave会不会自动挂载到那个master  

#### 节点间的通信机制

##### gossip协议

翻译过来是 小道流言

所有节点都持有一份元数据，不同的节点如果出现了元数据的变更之后，就不断将元数据发送给其他的节点，让其他节点也进行元数据的变更

跟集中式（比如zookeeper）不同的是，不是将集群元数据（节点信息，故障等等）集中存储在某个节点上，而是互相之间不断通信，保持整个集群所有节点的数据是完整的，

集中式  
优点： 元数据的更新和读取，实效性非常好，一旦元数据出现了变更，立即就更新到集中式的存储中，其他节点读取的时候立即就可以感知到  
缺点： 所有的元数据的更新压力全部集中在一个地方，可能会导致元数据的存储有压力

gossip：  
优点: 元数据的更新比较分散，不是集中在一起，更新请求会陆陆续续，打到所有的节点上去更新，有一定的延时，降低了压力  
缺点：元数据更新有延时，可能导致集群的一些操作会有一些滞后  

##### 10000端口号

每个节点都有一个专门用于节点间通信的端口，就是自己提供服务的端口号 + 10000，比如7001，那么用于节点间通信的端口就是17001

每个节点，每隔一段时间都会往另外几个节点发送ping消息，同时其他几点接收到ping之后返回pong

##### 交换的信息

节点间，交换的信息有 故障信息，节点的增加和移除，hash slot信息，等等


gossip协议包含多种消息，包括ping pong meet fail 等等

- meet 某个节点发送meet给新加入的节点，让心节点加入集群中，然后新节点就会开始与其他节点进行通信 `./redis-cli --cluster add-node` 命令其实内部就是发送了一个gossip meet消息，给新加入的节点，通知那个节点去加入我们的集群
- ping 每个节点都会频繁给其他节点发送ping 其中包含自己的状态还有自己维护的集群元数据，互相通过ping 交换元数据，每个节点每秒都会频繁发送ping给其他的集群，ping，频繁的互相之间交换数据，互相进行元数据的更新
- pong 返回ping和meet,包含自己的状态和其他信息，也可以用于信息广播和更新
- fail 某个节点判断另一个节点fail之后。就发送fail给其他节点，通知其他节点，指定的节点宕机了

##### ping消息深入

ping很频繁，而且要携带一些元数据，所以可能会加重网络负担。每个节点每秒会执行10次ping.每次会选择5个最久没有通信的其他节点，当然如果发现某个节点通信延时达到了cluster_node_timeout / 2，那么立即发送ping,避免数据交换延时过长，  
所以cluster_node_timeout可以调节,如果调节比较大，那么会降低发送的频率。每次ping，一个是带上自己节点的信息。还有就是带上1/10其他节点的信息。发送出去，进行数据交换。至少包含3个其他节点的信息。最多包含总节点-2个其他节点的信息


#### 高可用和主备切换原理

判断节点宕机

如果一个节点认为另外一个节点宕机，那就是pfail，主观宕机  
如果多个节点都认为另外一个节点宕机了，那么就是fail，客观宕机，跟哨兵的原理一样  
在`cluster-note-timeout`内，某个节点一直没有返回pong，那么就被任务pfail  
如果一个节点认为某个节点fail了，那么就会在gossip消息中，ping给其他节点，如果超过半数的节点都认为pfail了，那么就会变成fail

从节点过滤

对宕机的master node，从其所有的slave node中，选择一个切换成master node  
检查每个slave node与master node断开链接的时间，如果超过了cluster-node-timeout * cluster-slave-validity-factor ，那么就没有资格切换成master,这个跟哨兵的原理是一样的。  
每个从节点，都根据自己对master复制数据的offset，来设置一个选举时间，offset越大（复制数据越多）的从节点，选举时间越靠前，优先进行选举。  
所有的master node开始投票，给所有的slave进行投票，如果大部分master node (N/2 + 1) 都投票给了某个从节点，那么就选举通过，从节点执行主备切换，从节点切换为主节点  

与哨兵比较

整个流程跟哨兵相比，非常类似，所以说redis cluster功能强大，直接集成了replication和sentinal的功能

## 压测

### 工具

使用官方的redis-benchmark就可以了  
[官方文档](https://redis.io/docs/management/optimization/benchmarks/)

```shell
./redis-benchmark -h 127.0.0.1 -p 6379
```
## 常见问题和优化思路

### maxmemory-policy，
[Redis LRU官方文档](https://redis.io/topics/lru-cache)
可以设置内存达到最大闲置后，采取什么策略来处理 
1. noeviction: 如果内存使用达到了maxmemory，client还要继续写入数据，那么就直接报错给客户端
2. allkeys-lru: 就是我们常说的LRU算法，移除掉最近最少使用的那些keys对应的数据
3. volatile-lru: 也是采取LRU算法，但是仅仅针对那些设置了指定存活时间（TTL）的key才会清理掉
4. allkeys-random: 随机选择一些key来删除掉
5. volatile-random: 随机选择一些设置了TTL的key来删除掉
6. volatile-ttl: 移除掉部分keys，选择那些TTL时间比较短的keys

### fork耗时导致高并发请求延时

RDB和AOF的时候，其实会有生成RDB快照，AOF rewrite，耗费磁盘IO的过程，主进程fork子进程  
fork的时候，子进程是需要拷贝父进程的空间内存页表的，也是会耗费一定的时间的  
一般来说，如果父进程内存有1个G的数据，那么fork可能会耗费在20ms左右，如果是10G~30G，那么就会耗费20 * 10，甚至20 * 30，也就是几百毫秒的时间  
info stats中的latest_fork_usec，可以看到最近一次form的时长  
redis单机QPS一般在几万，fork可能一下子就会拖慢几万条操作的请求时长，从几毫秒变成1秒  

优化思路  
fork耗时跟redis主进程的内存有关系，一般控制redis的内存在10GB以内，slave -> master，全量复制  

### AOF的阻塞问题

redis将数据写入AOF缓冲区，单独开一个现场做fsync操作，每秒一次  
但是redis主线程会检查两次fsync的时间，如果距离上次fsync时间超过了2秒，那么写请求就会阻塞  
everysec，最多丢失2秒的数据  
一旦fsync超过2秒的延时，整个redis就被拖慢  

优化思路  
优化硬盘写入速度，建议采用SSD，不要用普通的机械硬盘，SSD，大幅度提升磁盘读写的速度

### 主从复制延迟问题

主从复制可能会超时严重，这个时候需要良好的监控和报警机制  
在info replication中，可以看到master和slave复制的offset，做一个差值就可以看到对应的延迟量  
如果延迟过多，那么就进行报警  

### 主从复制风暴问题

如果一下子让多个slave从master去执行全量复制，一份大的rdb同时发送到多个slave，会导致网络带宽被严重占用  
如果一个master真的要挂载多个slave，那尽量用树状结构，不要用星型结构  

### vm.overcommit_memory

- 0: 检查有没有足够内存，没有的话申请内存失败
- 1: 允许使用内存直到用完为止
- 2: 内存地址空间不能超过swap + 50%   
如果是0的话，可能导致类似fork等操作执行失败，申请不到足够的内存空间

```shell
cat /proc/sys/vm/overcommit_memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf
sysctl vm.overcommit_memory=1
```

### swapiness
cat /proc/version，查看linux内核版本  
如果linux内核版本<3.5，那么swapiness设置为0，这样系统宁愿swap也不会oom killer（杀掉进程）  
如果linux内核版本>=3.5，那么swapiness设置为1，这样系统宁愿swap也不会oom killer  

保证redis不会被杀掉

```shell
echo 0 > /proc/sys/vm/swappiness
echo vm.swapiness=0 >> /etc/sysctl.conf
```

### 最大打开文件句柄

```shell
ulimit -n 10032 10032
```

自己去上网搜一下，不同的操作系统，版本，设置的方式都不太一样

### tcp backlog

```shell
cat /proc/sys/net/core/somaxconn
echo 511 > /proc/sys/net/core/somaxconn
```

### 监控redis命令执行耗时
配置打印慢日志 一般redis单机qps可以达到几万 

### Pipline 或者lua脚本 批量执行命令
网络耗时是redis的性能瓶颈，内存操作非常快微妙级别的，网络操作就比较慢了ms级别的


### Redis连接池
Redis连接池，搞多个针对redis的链接

```config
## 最大等待获取连接的时间 通常不会超过1s
maxWaitMillis=
## 资源耗尽 是否立即失败 ，当false时，maxWaitMillis才会起作用
blockWhenExhausted=false
```

### Redis持久化

RDB和AOF Rewrite的持久化机制不要自动处理，而是放到半夜，系统负载低的时候再跑


### Linux 内存参数

```conf
vm.overcommit_memory=1
vm.swappiness=1
ulimit -Sn 
```

### Redis 性能问题
[一文讲透如何排查 Redis 性能问题！](https://heapdump.cn/article/3523071)

### Redis MONITOR命令 排查redis的性能
https://www.ipcpu.com/2021/07/redis-monitor-3/#:~:text=Redis%E4%B8%ADMONITOR%E5%91%BD%E4%BB%A4%E7%94%A8,%E8%BF%94%E5%9B%9E%E5%80%BC%E6%80%BB%E6%98%AFOK%E3%80%82

https://pdai.tech/md/db/nosql-redis/db-redis-y-monitor.html

[官方文档](https://redis.io/commands/monitor/)

搭配[redis-faina](https://github.com/facebookarchive/redis-faina)分析日志


数据样例：
```shell
1709621398.306134 [1 172.18.70.172:55316] "GET" "NOTIFICATION_IMG"
1709621398.306397 [1 172.18.70.179:46196] "HEXISTS" "nginx_log" "\x04>\x1cotJL05wjIShlwogRpcyfMkn_dllo"
1709621398.306415 [1 172.18.70.170:50418] "GET" "LOGIN:SALT:extension"
1709621398.307246 [1 172.18.70.172:55790] "GET" "USER:63f7lB8I7Off2KSN98rE2MZO"
```

其中第一个值为


# EOF