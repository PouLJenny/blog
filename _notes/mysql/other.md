# 零碎的小知识，需要整理

## Mysql操作JSON

### JSON数组去重问题

来自ChatGPT的去重复函数
```sql
CREATE FUNCTION JSON_UNIQ(arr JSON) RETURNS json READS SQL DATA
BEGIN
    DECLARE tempArr JSON DEFAULT JSON_ARRAY();
    DECLARE tempItem JSON DEFAULT NULL;
    DECLARE tempIndex INT DEFAULT NULL;
    DECLARE i INT DEFAULT 0;
    WHILE i < JSON_LENGTH(arr) DO
        SET tempItem = JSON_EXTRACT(arr, CONCAT('$[', i, ']'));
        IF NOT JSON_CONTAINS(tempArr, tempItem) THEN
            SET tempArr = JSON_INSERT(tempArr, CONCAT('$[', JSON_LENGTH(tempArr), ']'), tempItem);
        END IF;
        SET i = i + 1;
    END WHILE;

    RETURN tempArr;
END;
```

## mysql jdbc url格式及其支持的参数
[官方文档](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-jdbc-url-format.html)