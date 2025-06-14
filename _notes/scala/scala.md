# Scala

[官网](https://www.scala-lang.org/)


## 运行在JVM上

scala是运行在jvm上面的，所以也会编译成class文件。

比如我们声明一个scala文件,`Hello.scala`

```scala
object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello, Scala!")
  }
}
```

编译一下
```shell
scalac Hello.scala
```

编译完了之后，会发现会两个class文件
```shell
-rw-r--r--  1 poul poul  664  5月28日 10:16 'Hello$.class'
-rw-r--r--  1 poul poul  675  5月28日 10:16  Hello.class
-rw-r--r--  1 poul poul   92  5月28日 10:15  Hello.scala
```

可以使用`javap` 命令查询每个class文件中的内容

```shell
javap -c Hello
```
```asm
Compiled from "Hello.scala"
public final class Hello {
  public static void main(java.lang.String[]);
    Code:
       0: getstatic     #17                 // Field Hello$.MODULE$:LHello$;
       3: aload_0
       4: invokevirtual #19                 // Method Hello$.main:([Ljava/lang/String;)V
       7: return
}
```

```shell
javap -c Hello$
```
```asm
Compiled from "Hello.scala"
public final class Hello$ {
  public static final Hello$ MODULE$;

  public static {};
    Code:
       0: new           #2                  // class Hello$
       3: dup
       4: invokespecial #12                 // Method "<init>":()V
       7: putstatic     #14                 // Field MODULE$:LHello$;
      10: return

  public void main(java.lang.String[]);
    Code:
       0: getstatic     #22                 // Field scala/Predef$.MODULE$:Lscala/Predef$;
       3: ldc           #24                 // String Hello, Scala!
       5: invokevirtual #28                 // Method scala/Predef$.println:(Ljava/lang/Object;)V
       8: return
}
```


## 用java执行编译的scala类

直接执行
```shell
java Hello

Exception in thread "main" java.lang.NoClassDefFoundError: scala/Predef$
	at Hello$.main(Hello.scala:3)
	at Hello.main(Hello.scala)
Caused by: java.lang.ClassNotFoundException: scala.Predef$
	at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641)
	at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188)
	at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:525)
	... 2 more
```

可以看到出现了错误.

使用scala执行
```shell
scala Hello
Hello, Scala!
```

为啥会这样呢。
可以看一下scala命令脚本里面的内容
```bash
#!/usr/bin/env bash
#
##############################################################################
# Scala (https://www.scala-lang.org)
#
# Copyright EPFL and Lightbend, Inc. dba Akka
#
# Licensed under Apache License 2.0
# (http://www.apache.org/licenses/LICENSE-2.0).
#
# See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.
##############################################################################

findScalaHome () {
  # see scala/bug#2092 and scala/bug#5792
  local source="${BASH_SOURCE[0]}"
  while [ -h "$source" ] ; do
    local linked="$(readlink "$source")"
    local dir="$( cd -P "$(dirname "$source")" && cd -P "$(dirname "$linked")" && pwd )"
    source="$dir/$(basename "$linked")"
  done
  ( cd -P "$(dirname "$source")/.." && pwd )
}
execCommand () {
  [[ -n $SCALA_RUNNER_DEBUG ]] && echo "" && for arg in "$@"; do echo "$arg"; done && echo "";
  "$@"
}

# Not sure what the right default is here: trying nonzero.
scala_exit_status=127
saved_stty=""

# restore stty settings (echo in particular)
function restoreSttySettings() {
  if [[ -n $SCALA_RUNNER_DEBUG ]]; then
    echo "restoring stty:"
    echo "$saved_stty"
  fi

  stty $saved_stty
  saved_stty=""
}

function onExit() {
  [[ "$saved_stty" != "" ]] && restoreSttySettings
  exit $scala_exit_status
}

# to reenable echo if we are interrupted before completing.
trap onExit INT

# save terminal settings
saved_stty=$(stty -g 2>/dev/null)
# clear on error so we don't later try to restore them
if [[ ! $? ]]; then
  saved_stty=""
fi
if [[ -n $SCALA_RUNNER_DEBUG ]]; then
  echo "saved stty:"
  echo "$saved_stty"
fi

unset cygwin
if uname | grep -q ^CYGWIN; then
  cygwin="$(uname)"
fi

unset mingw
if uname | grep -q ^MINGW; then
  mingw="$(uname)"
fi

unset msys
if uname | grep -q ^MSYS; then
  msys="$(uname)"
fi

# Finding the root folder for this Scala distribution
SCALA_HOME="$(findScalaHome)"
SEP=":"

# Possible additional command line options
WINDOWS_OPT=""

# Remove spaces from SCALA_HOME on windows
if [[ -n "$cygwin" ]]; then
  SCALA_HOME="$(shome="$(cygpath --windows --short-name "$SCALA_HOME")" ; cygpath --unix "$shome")"
# elif uname |grep -q ^MINGW; then
#   SEP=";"
fi

# Constructing the extension classpath
TOOL_CLASSPATH=""
if [[ -z "$TOOL_CLASSPATH" ]]; then
    for ext in "$SCALA_HOME"/lib/* ; do
        file_extension="${ext##*.}"
        # scala/bug#8967 Only consider directories and files named '*.jar'
        if [[ -d "$ext" || $file_extension == "jar" ]]; then
          if [[ -z "$TOOL_CLASSPATH" ]]; then
              TOOL_CLASSPATH="$ext"
          else
              TOOL_CLASSPATH="${TOOL_CLASSPATH}${SEP}${ext}"
          fi
        fi
    done
fi

if [[ -n "$cygwin$mingw$msys" ]]; then
    case "$TERM" in
        rxvt* | xterm* | cygwin*)
            stty -icanon min 1 -echo
            WINDOWS_OPT="-Djline.terminal=unix"
        ;;
    esac
fi

[[ -n "$JAVA_OPTS" ]] || JAVA_OPTS="-Xmx256M -Xms32M"

# break out -D and -J options and add them to JAVA_OPTS as well
# so they reach the underlying JVM in time to do some good.  The
# -D options will be available as system properties.
declare -a java_args
declare -a scala_args

# scala/bug#8358, scala/bug#8368 -- the default should really be false,
# but I don't want to flip the default during 2.11's RC cycle
OVERRIDE_USEJAVACP="-Dscala.usejavacp=true"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -D*)
      # pass to scala as well: otherwise we lose it sometimes when we
      # need it, e.g. communicating with a server compiler.
      java_args+=("$1")
      scala_args+=("$1")
      # respect user-supplied -Dscala.usejavacp
      case "$1" in -Dscala.usejavacp*) OVERRIDE_USEJAVACP="";; esac
      shift
      ;;
    -J*)
      # as with -D, pass to scala even though it will almost
      # never be used.
      java_args+=("${1:2}")
      scala_args+=("$1")
      shift
      ;;
    -toolcp)
      TOOL_CLASSPATH="${TOOL_CLASSPATH}${SEP}${2}"
      shift 2
      ;;
    -nobootcp)
      usebootcp="false"
      shift
      ;;
    -usebootcp)
      usebootcp="true"
      shift
      ;;
    -debug)
      SCALA_RUNNER_DEBUG=1
      shift
      ;;
    *)
      scala_args+=("$1")
      shift
      ;;
  esac
done

# reset "$@" to the remaining args
set -- "${scala_args[@]}"

if [[ -n "$cygwin$mingw$msys" ]]; then
    if [[ "$OS" = "Windows_NT" ]] && cygpath -m .>/dev/null 2>/dev/null ; then
        format=mixed
    else
        format=windows
    fi
    SCALA_HOME="$(cygpath --$format "$SCALA_HOME")"
    if [[ -n "$JAVA_HOME" ]]; then
        JAVA_HOME="$(cygpath --$format "$JAVA_HOME")"
    fi
    TOOL_CLASSPATH="$(cygpath --path --$format "$TOOL_CLASSPATH")"
fi

if [[ -z "$JAVACMD" && -n "$JAVA_HOME" && -x "$JAVA_HOME/bin/java" ]]; then
    JAVACMD="$JAVA_HOME/bin/java"
fi

declare -a classpath_args

# default to the boot classpath for speed, except on cygwin/mingw/msys because
# JLine on Windows requires a custom DLL to be loaded.
if [[ "$usebootcp" != "false" && -z "$cygwin$mingw$msys" ]]; then
  usebootcp="true"
fi

# If using the boot classpath, also pass an empty classpath
# to java to suppress "." from materializing.
if [[ "$usebootcp" == "true" ]]; then
  classpath_args=("-Xbootclasspath/a:$TOOL_CLASSPATH" -classpath "\"\"")
  # Java 9 removed sun.boot.class.path, and the supposed replacement to at least see
  # the appended boot classpath (jdk.boot.class.path.append) is not visible.
  # So we have to pass a custom system property that PathResolver will find.
  # We do this for all JVM versions, rather than getting into the business of JVM version detection.
  classpath_args+=("-Dscala.boot.class.path=$TOOL_CLASSPATH")
else
  classpath_args=(-classpath "$TOOL_CLASSPATH")
fi

# Remove newline as delimiter for word splitting the java command.
# This permits the use case:
# export JAVA_OPTS=-Dline.separator=$'\r'$'\n'
# where otherwise the newline char is stripped after expansion.
# The following works with the default IFS:
# scala -J-Dline.separator=$'\r'$'\n'
IFS=" "$'\t'

# note that variables which may intentionally be empty must not
# be quoted: otherwise an empty string will appear as a command line
# argument, and java will think that is the program to run.
execCommand \
  "${JAVACMD:=java}" \
  $JAVA_OPTS \
  "${java_args[@]}" \
  "${classpath_args[@]}" \
  -Dscala.home="$SCALA_HOME" \
  $OVERRIDE_USEJAVACP \
  $WINDOWS_OPT \
   scala.tools.nsc.MainGenericRunner  "$@"

# record the exit status lest it be overwritten:
# then restore IFS, reenable echo and propagate the code.
scala_exit_status=$?

unset IFS

onExit
```


能看到，scala本质上也是调用了java执行的类方法，但是它会自动的帮助你封装一些参数。