inflation <- function(overTime, startYear, endYear){
  TARGET = 2
  THRESHOLD = 0.1
  TARGET_END = TARGET + THRESHOLD
  COLUMN_NAME = "PCEPILFE_PC1"
  table <- read.table("PCEPILFE.csv", header = TRUE, sep = ",")
  
  table <- table[seq(dim(table)[1],1),]

  count <- 1
  inflationOverTime <- c()
  xAxis <- c()
  index <- 1
  count <- 1
  firstIndex = -1;
  for (row in 1:nrow(table)) {
    date = table[row,"DATE"]
    if(as.numeric(substring(date, 1, 4)) > startYear){
    if(as.numeric(substring(date, 1, 4)) < endYear){
      if(firstIndex == -1){
        firstIndex = row
        count = firstIndex
      }
      
      sum <- 0
      rowValue = table[row, COLUMN_NAME]
      for(item in firstIndex:count){
        sum = sum + as.numeric(table[item, COLUMN_NAME])
      }
      
      avg = sum / index
      count <- count+1
    
      
      if(overTime){
        xAxis[index] = index
        inflationOverTime[index] = avg
      } else {
        xAxis[index] = date
        inflationOverTime[index] = rowValue
      }
      
      index <- index + 1
    }
    }
  }
  
  tableName = paste("Inflation, PCE (Ex. Food and Energy)","[",startYear, "; ", endYear-1, "]")
  xLabel = "Date"
  
  if(overTime){
    tableName = paste("Inflation Over Time, PCE (Ex. Food and Energy)","[",startYear, "; ", endYear-1, "]", "\n","Between: ", TARGET, " and ", TARGET_END, " %")   
    xLabel = "Months back"
  } else {
    print(xAxis[1])
  }
 
  
  if(overTime){
    barplot(height=inflationOverTime, 
            names=xAxis,
            col=ifelse(inflationOverTime >= TARGET & inflationOverTime <= TARGET_END ,"green","red2"), 
            main = tableName,
            xlab = xLabel,
            ylab = "%",
            ylim = c(-0.5,6))
  } else {
    barplot(height=inflationOverTime, 
            names=xAxis,
            col=ifelse(inflationOverTime >= TARGET,"red","red2"), 
            main = tableName,
            xlab = xLabel,
            ylab = "%",
            ylim = c(-0.5,6))
    
    
  }
  
  
  abline(h = TARGET,
         col = "blue",
         lty = "dashed",
         lwd = 1)
  
  if(overTime){
    abline(h = TARGET_END,
         col = "blue",
         lty = "dashed",
         lwd = 1)
  }

  
}


inflation(TRUE,2005, 2025)
