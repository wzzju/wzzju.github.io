---
layout: post
title: "使用Maven构建Hadoop MapReduce工程"
date: 2017-07-07
comments: true
categories: [ "Hadoop", "Maven" ]
---

###### 1.执行如下命令创建maven工程：
```bash
mvn archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes -DgroupId=top.wzzju.temperature -DartifactId=temperature
```
一路回车，直到maven项目创建完成。

###### 2.修改pom.xml文件

```bash
cd temperature
vim pom.xml
#修改内容如下(其中的temperature需要根据实际项目的groupId和artifactId来修改)：
```

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>top.wzzju.temperature</groupId>
  <artifactId>temperature</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>

  <name>temperature</name>
  <url>http://maven.apache.org</url>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>2.3.2</version>
        <configuration>
          <archive>
            <manifest>
              <addClasspath>true</addClasspath>
              <mainClass>top.wzzju.temperature.Temperature</mainClass>
            </manifest>
          </archive>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>2.3.2</version>
        <configuration>
          <source>1.7</source>
          <target>1.7</target>
        </configuration>
      </plugin>
     </plugins>
  </build>

  <dependencies>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-hdfs</artifactId>
      <version>2.6.0</version>
    </dependency>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-mapreduce-client-jobclient</artifactId>
      <version>2.6.0</version>
    </dependency>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-common</artifactId>
      <version>2.6.0</version>
    </dependency>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

</project>

```

###### 3.根据自己的MapReduce工作进行修改源码：

```bash
cd temperature
mv src/main/java/top/wzzju/temperature/App.java  src/main/java/top/wzzju/temperature/Temperature.java
vim src/main/java/top/wzzju/mrcount/Temperature.java
```

**MapReduce程序模板如下：**

```java
package top.wzzju.temperature;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class Temperature extends Configured implements Tool {
    /**
     * 四个泛型类型分别代表：
     * KeyIn        Mapper的输入数据的Key，这里是每行文字的起始位置（0,11,...）
     * ValueIn      Mapper的输入数据的Value，这里是每行文字
     * KeyOut       Mapper的输出数据的Key，这里是每行文字中的“年份”
     * ValueOut     Mapper的输出数据的Value，这里是每行文字中的“气温”
     */
    public static class TempMapper extends
            Mapper<LongWritable, Text, Text, IntWritable> {
//        @Override
//        public void setup(Context context) {
//          /* setup any configs from the command line */
//          this.val = context.getConfiguration().get("some.value");
//        }
        @Override
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            // 打印样本: Before Mapper: 0, 2000010115
            System.out.print("Before Mapper: " + key + ", " + value);
            String line = value.toString();
            String year = line.substring(0, 4);
            int temperature = Integer.parseInt(line.substring(8));
            context.write(new Text(year), new IntWritable(temperature));
            // 打印样本: After Mapper:2000, 15
            System.out.println(
                    "======" +
                    "After Mapper:" + new Text(year) + ", " + new IntWritable(temperature));
        }
    }
    /**
     * 四个泛型类型分别代表：
     * KeyIn        Reducer的输入数据的Key，这里是每行文字中的“年份”
     * ValueIn      Reducer的输入数据的Value，这里是每行文字中的“气温”
     * KeyOut       Reducer的输出数据的Key，这里是不重复的“年份”
     * ValueOut     Reducer的输出数据的Value，这里是这一年中的“最高气温”
     */
    public static class TempReducer extends
            Reducer<Text, IntWritable, Text, IntWritable> {
        @Override
        public void reduce(Text key, Iterable<IntWritable> values,
                Context context) throws IOException, InterruptedException {
            int maxValue = Integer.MIN_VALUE;
            StringBuffer sb = new StringBuffer();
            //取values的最大值
            for (IntWritable value : values) {
                maxValue = Math.max(maxValue, value.get());
                sb.append(value).append(", ");
            }
            // 打印样本： Before Reduce: 2000, 15, 23, 99, 12, 22,
            System.out.print("Before Reduce: " + key + ", " + sb.toString());
            context.write(key, new IntWritable(maxValue));
            // 打印样本： After Reduce: 2000, 99
            System.out.println(
                    "======" +
                    "After Reduce: " + key + ", " + maxValue);
        }
    }

    @Override
    public int run(String[] allArgs) throws Exception {
        Job job = Job.getInstance(getConf());

        job.setJarByClass(Temperature.class);
        // basic I/O shape setup
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // map, combine, partition, reduce setup
        job.setMapperClass(TempMapper.class);
        //job.setCombinerClass(MyCombiner.class);
        job.setReducerClass(TempReducer.class);
        //job.setNumReduceTasks(1);

        // parse options passed to the job
        String[] args = new GenericOptionsParser(
                getConf(), allArgs).getRemainingArgs();
        // set the files (from arguments)
        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        // wait for the jobs to finish
        boolean status = job.waitForCompletion(true);
        return status ? 0 : 1;

    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        ToolRunner.run(new Temperature(), args);
    }
}

```

###### 4.编译和打包命令

```bash
cd temperature
mvn clean install
```

###### 5.在hadoop上执行

```bash
cd temperature
# 每次运行输出目录不可以重复
hadoop jar target/temperature-1.0-SNAPSHOT.jar /yuchen/root/*.txt /yuchen/root/temerature_out
# or
hadoop jar target/temperature-1.0-SNAPSHOT.jar /yuchen/root/input.txt /yuchen/root/temerature_out
```

###### 6.查看运行结果

```bash
hadoop fs -ls /yuchen/root/temerature_out
hadoop fs -cat  /yuchen/root/temerature_out/part-r-00000
```

###### 7.vim命令

* `Shift+g`跳转到最后
* `gg`跳转到第一行
* `Ctrl+r`重做（redo）

###### 8. maven命令

* 打包：`mvn package`
* 编译：`mvn compile`
* 编译测试程序：`mvn test-compile`
* 清空：`mvn clean`
* 运行测试：`mvn test`
* 生成站点目录: `mvn site`
* 生成站点目录并发布：`mvn site-deploy`
* 安装当前工程的输出文件到本地仓库: `mvn install`
* 先清空再安装：`mvn clean install`
* 生成eclipse工程文件：`mvn eclipse:eclipse`
* 运行jar包：`java -cp target/mrdemo-1.0-SNAPSHOT.jar top.wzzju.App`

###### 9. 使用python运行MapReduce程序命令

```bash
export STREAM=$HADOOP_PREFIX/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar

hadoop jar $STREAM -files ./mapper.py,./reducer.py -mapper ./mapper.py -reducer ./reducer.py -input /yuchen/root/zen10.txt -output /yuchen/root/zen_out
```

###### 10.参考资料

* [Hadoop 2 (2.2.0) setup on Debian](https://tuttlem.github.io/2014/01/09/hadoop-2-2-2-0-setup-on-debian.html)

* [Hadoop Links](https://tuttlem.github.io/2014/01/10/hadoop-links.html)

* [File System Shell Guide](http://hadoop.apache.org/docs/r2.6.0/hadoop-project-dist/hadoop-common/FileSystemShell.html)

* [Create a MapReduce Job using Java and Mave](https://tuttlem.github.io/2014/
01/30/create-a-mapreduce-job-using-java-and-maven.html)

* [Hadoop job setup](https://tuttlem.github.io/2015/12/02/hadop-job-setup.html
)

* [Hadoop Streaming with Python](https://tuttlem.github.io/2015/11/21/hadoop-s
treaming-with-python.html)

* [Custom text delimiters in Hadoop jobs](https://tuttlem.github.io/2015/11/26
/custom-text-delimiters-in-hadoop-jobs.html)

* [Hadoop MapReduce执行过程详解（带hadoop例子）](https://my.oschina.net/itblog/blog/275294)

* [vim 常用快捷键 二](http://www.cnblogs.com/wangkangluo1/archive/2012/04/12/2444952.html)

