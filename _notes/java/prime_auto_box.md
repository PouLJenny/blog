# 基本类型的自动拆装箱


都知道java中的基本类型会自动拆装箱，但是是怎么做到这一点的呢。


首先，写一个自动拆装箱的例子:

```java
public class PrimeAutoBox {
    public static void main(String[] args) {
        Byte b1 = (byte)1; // 自动装箱
        byte b2 = b1; // 自动拆箱

        Short s1 = (short)1;
        short s2 = s1;

        Integer i1 = 1;
        int i2 = i1;

        Long l1 = 1L;
        Long l2 = l1;

        Float f1 = (float) 0.1;
        Float f2 = f1;

        Double d1 = 0.1;
        double d2 = d1;

        Character c1 = '1';
        char c2 = c1;

        Boolean bl1 = false;
        boolean bl2 = bl1;
    }
}
```

编译一下
```shell
javac PrimeAutoBox.java
```

查看编译后的代码:

```shell
javap -c PrimeAutoBox
```

结果
```asm
Compiled from "PrimeAutoBox.java"
public class PrimeAutoBox {
  public PrimeAutoBox();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static void main(java.lang.String[]);
    Code:
       0: iconst_1
       1: invokestatic  #7                  // Method java/lang/Byte.valueOf:(B)Ljava/lang/Byte;
       4: astore_1
       5: aload_1
       6: invokevirtual #13                 // Method java/lang/Byte.byteValue:()B
       9: istore_2
      10: iconst_1
      11: invokestatic  #17                 // Method java/lang/Short.valueOf:(S)Ljava/lang/Short;
      14: astore_3
      15: aload_3
      16: invokevirtual #22                 // Method java/lang/Short.shortValue:()S
      19: istore        4
      21: iconst_1
      22: invokestatic  #26                 // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      25: astore        5
      27: aload         5
      29: invokevirtual #31                 // Method java/lang/Integer.intValue:()I
      32: istore        6
      34: lconst_1
      35: invokestatic  #35                 // Method java/lang/Long.valueOf:(J)Ljava/lang/Long;
      38: astore        7
      40: aload         7
      42: astore        8
      44: ldc           #40                 // float 0.1f
      46: invokestatic  #41                 // Method java/lang/Float.valueOf:(F)Ljava/lang/Float;
      49: astore        9
      51: aload         9
      53: astore        10
      55: ldc2_w        #46                 // double 0.1d
      58: invokestatic  #48                 // Method java/lang/Double.valueOf:(D)Ljava/lang/Double;
      61: astore        11
      63: aload         11
      65: invokevirtual #53                 // Method java/lang/Double.doubleValue:()D
      68: dstore        12
      70: bipush        49
      72: invokestatic  #57                 // Method java/lang/Character.valueOf:(C)Ljava/lang/Character;
      75: astore        14
      77: aload         14
      79: invokevirtual #62                 // Method java/lang/Character.charValue:()C
      82: istore        15
      84: iconst_0
      85: invokestatic  #66                 // Method java/lang/Boolean.valueOf:(Z)Ljava/lang/Boolean;
      88: astore        16
      90: aload         16
      92: invokevirtual #71                 // Method java/lang/Boolean.booleanValue:()Z
      95: istore        17
      97: return
}
```


以Integer为例子，能看到，自动装箱的代码是走的`Integer.valueOf()`方法，自动拆箱走的是`Integer.intValue()`方法.


所以本质上基本类型的拆装箱，是一种语法糖，编译阶段会处理这种语法糖。jvm层面是不知道有自动拆装箱的.


## 缓存

java对一些基本类型的包装类做了缓存处理，可以复用对象，防止对象的频繁创建和销毁.做这个操作就是在自动装箱，调用`Integer.valueOf()`的时候触发的.下面可以针对每个类型分别看一下


### Byte

```java
public static Byte valueOf(byte b) {
    final int offset = 128;
    return ByteCache.cache[(int)b + offset];
}


private static class ByteCache {
    private ByteCache() {}

    static final Byte[] cache;
    static Byte[] archivedCache;

    static {
        final int size = -(-128) + 127 + 1;

        // Load and use the archived cache if it exists
        CDS.initializeFromArchive(ByteCache.class);
        if (archivedCache == null || archivedCache.length != size) {
            Byte[] c = new Byte[size];
            byte value = (byte)-128;
            for(int i = 0; i < size; i++) {
                c[i] = new Byte(value++);
            }
            archivedCache = c;
        }
        cache = archivedCache;
    }
}
```
可以看到`byte`做了-128 ～ 127 所有值的缓存


### Short

```java
public static Short valueOf(short s) {
    final int offset = 128;
    int sAsInt = s;
    if (sAsInt >= -128 && sAsInt <= 127) { // must cache
        return ShortCache.cache[sAsInt + offset];
    }
    return new Short(s);
}

private static class ShortCache {
    private ShortCache() {}

    static final Short[] cache;
    static Short[] archivedCache;

    static {
        int size = -(-128) + 127 + 1;

        // Load and use the archived cache if it exists
        CDS.initializeFromArchive(ShortCache.class);
        if (archivedCache == null || archivedCache.length != size) {
            Short[] c = new Short[size];
            short value = -128;
            for(int i = 0; i < size; i++) {
                c[i] = new Short(value++);
            }
            archivedCache = c;
        }
        cache = archivedCache;
    }
}
```

可以看到`short`也是做了-128 ～ 127 值的缓存

### Integer

```java
public static Integer valueOf(int i) {
    if (i >= IntegerCache.low && i <= IntegerCache.high)
        return IntegerCache.cache[i + (-IntegerCache.low)];
    return new Integer(i);
}


private static class IntegerCache {
    static final int low = -128;
    static final int high;
    static final Integer[] cache;
    static Integer[] archivedCache;

    static {
        // high value may be configured by property
        int h = 127;
        String integerCacheHighPropValue =
            VM.getSavedProperty("java.lang.Integer.IntegerCache.high");
        if (integerCacheHighPropValue != null) {
            try {
                h = Math.max(parseInt(integerCacheHighPropValue), 127);
                // Maximum array size is Integer.MAX_VALUE
                h = Math.min(h, Integer.MAX_VALUE - (-low) -1);
            } catch( NumberFormatException nfe) {
                // If the property cannot be parsed into an int, ignore it.
            }
        }
        high = h;

        // Load IntegerCache.archivedCache from archive, if possible
        CDS.initializeFromArchive(IntegerCache.class);
        int size = (high - low) + 1;

        // Use the archived cache if it exists and is large enough
        if (archivedCache == null || size > archivedCache.length) {
            Integer[] c = new Integer[size];
            int j = low;
            for(int i = 0; i < c.length; i++) {
                c[i] = new Integer(j++);
            }
            archivedCache = c;
        }
        cache = archivedCache;
        // range [-128, 127] must be interned (JLS7 5.1.7)
        assert IntegerCache.high >= 127;
    }

    private IntegerCache() {}
}
```

可以看到`int`的机制相对来说复杂一点，默认是缓存 -128 ~ 127 之间的数字。但是可以通过启动参数的方式扩大`high`的值 `-Djava.lang.Integer.IntegerCache.high=1000`


### Long

```java
public static Long valueOf(long l) {
    final int offset = 128;
    if (l >= -128 && l <= 127) { // will cache
        return LongCache.cache[(int)l + offset];
    }
    return new Long(l);
}


private static class LongCache {
    private LongCache() {}

    static final Long[] cache;
    static Long[] archivedCache;

    static {
        int size = -(-128) + 127 + 1;

        // Load and use the archived cache if it exists
        CDS.initializeFromArchive(LongCache.class);
        if (archivedCache == null || archivedCache.length != size) {
            Long[] c = new Long[size];
            long value = -128;
            for(int i = 0; i < size; i++) {
                c[i] = new Long(value++);
            }
            archivedCache = c;
        }
        cache = archivedCache;
    }
}
```

可以看到 `long`也是缓存的 -128 ~ 127 之间的数字


### Float

```java
public static Float valueOf(float f) {
    return new Float(f);
}
```

可以看到`float`没有缓存


### Double

```java
public static Double valueOf(double d) {
    return new Double(d);
}
```
可以看到`double`也没有缓存


### Character

```java
public static Character valueOf(char c) {
    if (c <= 127) { // must cache
        return CharacterCache.cache[(int)c];
    }
    return new Character(c);
}

private static class CharacterCache {
    private CharacterCache(){}

    static final Character[] cache;
    static Character[] archivedCache;

    static {
        int size = 127 + 1;

        // Load and use the archived cache if it exists
        CDS.initializeFromArchive(CharacterCache.class);
        if (archivedCache == null || archivedCache.length != size) {
            Character[] c = new Character[size];
            for (int i = 0; i < size; i++) {
                c[i] = new Character((char) i);
            }
            archivedCache = c;
        }
        cache = archivedCache;
    }
}
```

可以看到`char`缓存的是`0 ~ 127`的值


### Boolean 

```java
/**
 * The {@code Boolean} object corresponding to the primitive
 * value {@code true}.
 */
public static final Boolean TRUE = new Boolean(true);

/**
 * The {@code Boolean} object corresponding to the primitive
 * value {@code false}.
 */
public static final Boolean FALSE = new Boolean(false);

public static Boolean valueOf(boolean b) {
    return (b ? TRUE : FALSE);
}
```    

可以看到`boolean`也缓存了true和false的值
