if [ $? -eq 0 ]; then
    grep "Timing-tstoragefile-write-totalMegabytes" report.xml 
    if [ $? -eq 0 ]; then
        events=$(grep "<EventsRead>" report.xml | tail -1 | sed "s/.*>\(.*\)<.*/\1/")
        size=$(grep "Timing-tstoragefile-write-totalMegabytes" report.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
        if [ $events -gt 0 ]; then
            echo "Size/event: $(bc -l <<< "scale=4; $size*1024 / $events")"
        fi
    fi
fi
grep "EventThroughput" report.xml 
if [ $? -eq 0 ]; then
  var1=$(grep "EventThroughput" report.xml | sed "s/.* Value=\"\(.*\)\".*/\1/")
  echo "time_event value: $(bc -l <<< "scale=4; 1/$var1")"
fi
echo CPU efficiency info:
grep "TotalJobCPU" report.xml 
grep "TotalJobTime" report.xml 
grep "PeakValue" report.xml 
