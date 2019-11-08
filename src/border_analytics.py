import sys
import csv
import operator 
def main(datapath='../input/Border_Crossing_Entry_Data.csv',outputpath='../output/report.csv'):
    def read(datapath):
        #fields = []
        rows  = []
        with open(datapath,'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                rows.append(row)
            #print('total row numers:', len(rows))
            # sort by date, border  measure
            process = rows
            sorted(process,key=operator.itemgetter(4,3,5))
        # add missing fileds
        #fields += ['Location']
        return process


    def question1(rd1):
        sort_rows=rd1
        q1={}
        # q1 = {date:{measure:[value,mean]}}
        date,measure,value = 4,5,6
        for item in sort_rows:
            if q1.get(item[date]) is None:  # store new date 
                q1[item[date]]={item[measure]:int(item[value])} 
            #if measure is new
            elif q1[item[date]].get(item[measure]) is None: 
                #add measure, crossing value and initialize count
                q1[item[date]][item[measure]]=int(item[value]) 
            #sum up crossing values for same date, measure, border     
            else:q1[item[date]][item[measure]] += int(item[value])  
        #print(q1) 
        # total number of crossings (Value) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used.
        print('solved 1st question')
        return q1

    def question2(rd,q1):
        # b: border -> measure ->time ->value 
        # b= {border:{measure:{date:[preSumValue,mean,currentValue]}}}
        b={}
        q1 = q1
        # count number of entries for b
        ct=0 
        date,measure,border,value = 4,5,3,6,
        sort_rows   = rd
        date_set  = set()
        border_set  = set()
        measure_set = set()
        l_changed= []
        date_dict = {} 
        for item in sort_rows:
            date_set.add(item[date])
            border_set.add(item[border])
            measure_set.add(item[measure])
        #print(len(date_set))

        l = list(date_set)
        for x in l:
            x=x[:10]
            l_changed.append(x)
        l_changedx = [i.split('/') for i in l_changed]
        #sort date by year and month 
        date_sorted = sorted(l_changedx,key=operator.itemgetter(2,0)) 
        #print(date_sorted)
        #transform sorted date into raw date entry,and spare additional entry for mean
        date_sort_join=[]
        index = 0
        rest_date_format = l[0][10:]
        for i in date_sorted:
            i = '/'.join(i)
            date_sort_join.append((i+rest_date_format,index))
            index += 1
        for j in date_sort_join:
            date_dict[j[0]]=j[1]
        for item in sort_rows:
            # border is new 
            if b.get(item[border]) is None:
                #if item[] 
                b[item[border]]={item[measure]:{item[date]:[int(item[value]),0,int(item[value])]}}
            #if border is new
            if b[item[border]].get(item[measure]) is None:  
                # add measure, crossing value and initialize count
                b[item[border]][item[measure]]={item[date]:[int(item[value]),0,int(item[value])]}  
            # if date is new
            if b[item[border]][item[measure]].get(item[date]) is None:   
                b[item[border]][item[measure]][item[date]]=[int(item[value]),0,int(item[value])]   
            if date_dict[item[date]] != 0: 
                try:
                    b[item[border]][item[measure]][item[date]][0] = int(q1[item[date]][item[measure]][0])
                    #b[item[border]][item[measure]][item[date]][0] += int(item[value])/date_dict[item[date]] 
                    #b[item[border]][item[measure]][item[date]][1] = round(b[item[border]][item[measure]][item[date]][0]+int(b[item[border]][item[measure]][item[date]][2])/int(date_dict[item[date]])) # mean
                    b[item[border]][item[measure]][item[date]][1] = round(q1[item[date]][item[measure]][0]/int(date_dict[item[date]]))
                    #b[item[border]][item[measure]][item[date]][1] = c
                except:
                    
                    print("devision overflow")
                   # print(c)
            ct += 1
        #print("number of b: ",ct)
        out = []
        for borderx in border_set:
            for measurex in measure_set:
                for x in range(len(date_sort_join)):
                    Date  = date_sort_join[x][0]
                   # Mean  = b[borderx][measurex][date_sort_join[x][0]][1]
                    #Value = b[borderx][measurex][date_sort_join[x][0]][2]
                    try:
                        if b is not None and b.get(borderx) is not None and b[borderx].get(measurex) is not None and b[borderx][measurex].get(Date) is not None:
                            out.append([borderx, date_sort_join[x][0], measurex, b[borderx][measurex][date_sort_join[x][0]][2], b[borderx][measurex][date_sort_join[x][0]][1]])
                    except:
                        print("KeyError")
        #print('solved 2nd question')
        return out
    
    def writeToCSV(q2):
        out2 = sorted(q2,key=lambda k2:(k2[1],k2[3],k2[2],k2[0]),reverse=True)
        with open(outputpath,mode='w',newline='') as f1:
            fieldnames = ['Border','Date','Measure','Value','Average']
            writer = csv.DictWriter(f1,fieldnames=fieldnames)
            writer.writeheader()
            for i in out2:
                writer.writerow({'Border':i[0],'Date':i[1],'Measure':i[2],'Value':i[3],'Average':i[4]})
        print("write success")
        #return out2

    z=question1(read(datapath))
    y = question2(read(datapath),z)
    writeToCSV(y)


if __name__=='__main__':
    if len(sys.argv) != 3:
        print("please input data path and output path")
        sys.exit(1)
    sys.exit(main(*sys.argv[1:]))
