import os
import json
import csv

## Convert the tunable configs of JDK and Quarkus generated by HPO to JDK_JAVA_OPTIONS
## Input: HPO config json
## Output: JDK_JAVA_OPTIONS
def get_envoptions(hpoconfigjson):
    tunables_jvm_boolean = ["TieredCompilation", "AllowParallelDefineClass", "AllowVectorizeOnDemand", "AlwaysCompileLoopMethods", "AlwaysPreTouch", "AlwaysTenure", "BackgroundCompilation", "DoEscapeAnalysis", "UseInlineCaches", "UseLoopPredicate", "UseStringDeduplication", "UseSuperWord", "UseTypeSpeculation"]
    tunables_jvm_values = ["FreqInlineSize", "MaxInlineLevel", "MinInliningThreshold", "CompileThreshold", "CompileThresholdScaling", "ConcGCThreads", "InlineSmallCode", "LoopUnrollLimit", "LoopUnrollMin", "MinSurvivorRatio", "NewRatio", "TieredStopAtLevel"]
    tunables_quarkus = ["quarkus.thread-pool.core-threads", "quarkus.thread-pool.queue-size", "quarkus.datasource.jdbc.min-size", "quarkus.datasource.jdbc.max-size"]
    JDK_JAVA_OPTIONS = ""

    with open(hpoconfigjson) as data_file:
        sstunables = json.load(data_file)

    for st in sstunables:
        for btunable in tunables_jvm_boolean:
            if btunable == st["tunable_name"]:
                if st["tunable_value"] == "true":
                    JDK_JAVA_OPTIONS = JDK_JAVA_OPTIONS + " -XX:+" + btunable
                elif st["tunable_value"] == "false":
                    JDK_JAVA_OPTIONS = JDK_JAVA_OPTIONS + " -XX:-" + btunable

        for jvtunable in tunables_jvm_values:
            if jvtunable == st["tunable_name"]:
                if jvtunable == "ConcGCThreads":
                    ## To avoid JVM exit if ParallelGCThreads < ConcGCThreads.
                    ## Only until dependencies between tunables are set.
                    JDK_JAVA_OPTIONS = JDK_JAVA_OPTIONS + " -XX:" + jvtunable + "=" + str(st["tunable_value"]) + " -XX:ParallelGCThreads=" + str(st["tunable_value"])
                else:
                    JDK_JAVA_OPTIONS = JDK_JAVA_OPTIONS + " -XX:" + jvtunable + "=" + str(st["tunable_value"])
                
        for qtunable in tunables_quarkus:
            if qtunable == st["tunable_name"]:
                JDK_JAVA_OPTIONS = JDK_JAVA_OPTIONS + " -D" + qtunable + "=" + str(st["tunable_value"])

    print(str(JDK_JAVA_OPTIONS))
