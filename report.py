# some calculations about corona values
# start date somewhen in 3/2020
# added multiprocessing in 6/2020

import pandas as pd 
import matplotlib.pyplot as plt 
from multiprocessing import Process 

# process files with these suffixes
localSuffixes = ["BW", "BY", "GER", "WORLD", "US"]

# flexinterval
flexInt = 7

def processWorker(localSuffix):
    print (f"------ processing {localSuffix} -----\n")

    #set the filename to process
    dataFile = "coronaData_" + localSuffix + ".csv"

    # read the data
    total = pd.read_csv(dataFile)

    # calculate the difference of totals

    i = 0
    # StillInfected - no of people infected but not curated
    # Diff - no of new infections from last value
    # percent - percentage of new infections from StillInfected (ratio)
    # DiffDiff - change of change (difference of changes from last change value to today)
    AktDiff = pd.DataFrame(columns=['StillInfected', 'Diff', 'Percent', 'DiffDiff'])
    lastDiff = 0
    # go through all values and calculate the addiional kpis for each day
    for x in range(len(total)):

        # get actual Number of infected people
        aktval=total.iloc[i]['Total']
        if (i != 0):
            lastval=total.iloc[i-1]['Total']
        else:
            lastval = 0

        # get actual Number of curated people
        aktCurated=total.iloc[i]['Curated']
        if (i != 0):
            lastCurated=total.iloc[i-1]['Curated']
        else:
            lastCurated = 0

       
        # number of deaths
        aktDeaths=total.iloc[i]['Deaths']
        
        # calculate number of still Infected
        stillInfected = aktval - aktCurated - aktDeaths

        # calculate difference between last value and actual value
        diff=aktval-lastval

        lastStillInfected = lastval - lastCurated


        # calculate percentage of change (how much new infected people in relation to still infected) in relation to last value
        if (lastStillInfected != 0):
            percent=(diff) / lastStillInfected *100
        else:
            #if first value, set to zero
            percent=0

        # calculate difference of difference (2nd diff)
        DiffDiff = diff-lastDiff
        lastDiff = diff

        # calculate relative rate to last week (assumption: incubation time approx 5 days, people who are positive will not infect more)
        if (i > 7):
            infectedLastWeek = AktDiff.iloc[i-5]['StillInfected']
            if (infectedLastWeek != 0):
                relInfectedToLastWeek = diff / infectedLastWeek *100
            else: 
                relInfectedToLastWeek = 0
        else:
            infectedLastWeek = 0
            relInfectedToLastWeek = 0

        # copy last 30 days in container relInfectedToLastWeek30
        if (i > len(total)-20):
            relInfectedToLastWeek20 = relInfectedToLastWeek
        else:
            relInfectedToLastWeek20 = 0

        # calculate "reproduction" rate
        if (i > 7):
            #sum of new Infections day -8 to -5
            sum4Infected1 = 0
            #sum of new Infections day -4 to -1
            sum4Infected2 = 0
            # calculate the sum of new infections day -8 to -5 (they might not know that they are infected the day before)
            # be careful with the index! we are in day -1, because the array is not yet written so index (i) is today, but not present
            for k in range(4):
                sum4Infected1 =sum4Infected1 + AktDiff.iloc[i-k-5]['Diff']          
            # calculate the sum of new infections day -4 to -1 (they might not know that they are infected the day before)
            for k in range(3):
                 sum4Infected2 =sum4Infected2 + AktDiff.iloc[i-k-1]['Diff']
            # add the number for today
            sum4Infected2 = sum4Infected2 + diff
            # calculate reproduction rate     
            reproRate = sum4Infected2 / sum4Infected1
        else:
            reproRate = 0
    
        # copy last 30 days in container reproRate30
        if (i > len(total)-20):
            reproRate20 = reproRate
        else:
            reproRate20 = 0

        # calculate "reproductionflex" rate

        if (i > (2*flexInt)-1):
            #sum of new Infections day -2xflexint to -flexint
            sumFlexInfected1 = 0
            #sum of new Infections day flexint to -1
            sumFlexInfected2 = 0
            # calculate the sum of new infections day -8 to -5 (they might not know that they are infected the day before)
            # be careful with the index! we are in day -1, because the array is not yet written so index (i) is today, but not present
            for k in range(flexInt):
                sumFlexInfected1 =sumFlexInfected1 + AktDiff.iloc[i-k-flexInt-1]['Diff']          
            # calculate the sum of new infections day -4 to -1 (they might not know that they are infected the day before)
            for k in range(flexInt-1):
                 sumFlexInfected2 =sumFlexInfected2 + AktDiff.iloc[i-k-1]['Diff']
            # add the number for today
            sumFlexInfected2 = sumFlexInfected2 + diff
            # calculate reproduction rate     
            reproFlexRate = sumFlexInfected2 / sumFlexInfected1
        else:
            reproFlexRate = 0
    
        # copy last 30 days in container reproRate30
        if (i > len(total)-20):
            reproFlexRate20 = reproFlexRate
        else:
            reproFlexRate20 = 0

        AktDiff = AktDiff.append({'reproRate' : reproRate, 'reproRate20' : reproRate20,'reproFlexRate' : reproFlexRate, 'reproFlexRate20' : reproFlexRate20, 'relInfectedToLastWeek' : relInfectedToLastWeek, 'relInfectedToLastWeek20' : relInfectedToLastWeek20, 'StillInfected' : stillInfected, 'Diff' : diff, 'Percent': percent, 'DiffDiff' : DiffDiff}, ignore_index=True)

        i=i+1

    # add the calculated kpis to the values matrix
    outValue = pd.concat([total , AktDiff], axis=1)
 
    # create some nice charts
    SMALL_SIZE = 6
    MEDIUM_SIZE = 8
    BIGGER_SIZE = 8

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    # get values of last date in strings
    lastDate = str(outValue.iloc[-1]['Date'])
    lastTotal = str(outValue.iloc[-1]['Total'])
    lastCurated = str(outValue.iloc[-1]['Curated'])
    lastDeaths = str(outValue.iloc[-1]['Deaths'])
    lastStillInfected = f"{outValue.iloc[-1]['StillInfected']:.0f}"

    print(f"Last date: {lastDate}\n")

    # ------------ first chart (containing of 4 subplots) ----------------
    fig, axes = plt.subplots(4,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False)
    axes[2].xaxis.set_visible(False)

    # subchart 1: total
    outValue.plot(x='Date', y='Total', ax=axes[0], title='data taken from Berliner Morgenpost - ' + dataFile + " (" + lastDate + ")" +'\n\nAnzahl Infizierte (akt. Wert: ' + lastTotal + ")")
    axes[0].get_legend().remove()

    # subchart 2: curated
    outValue.plot(x='Date', y='Curated', color='green', ax=axes[1], title='Anzahl wieder gesund (akt. Wert: ' + lastCurated + ")")
    axes[1].get_legend().remove()

    # subchart 3: deaths
    outValue.plot(x='Date', y='Deaths', color='black', ax=axes[2], title='Anzahl Tote (akt. Wert: ' + lastDeaths + ")")
    axes[2].get_legend().remove()

    # subchart 4: stillInfected
    outValue.plot(x='Date', y='StillInfected', color='red', ax=axes[3], title='Anzahl noch infiziert (akt. Wert: ' + lastStillInfected + ")")
    axes[3].get_legend().remove()

    # autoformat the layout to fit
    plt.tight_layout()
    # save it in a file 
    plt.savefig("Absolute_Values_" + localSuffix + ".png", dpi=300)

    # ------------ second chart (containing of 3 subplots): the calculated values -------------
    # get values of last date in strings
    lastPercent = f"{outValue.iloc[-1]['Percent']:.2f}"
    lastDiff = f"{outValue.iloc[-1]['Diff']:.0f}"
    lastDiffDiff = f"{outValue.iloc[-1]['DiffDiff']:.0f}"
    
    
    fig, axes = plt.subplots(3,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False)
 
    outValue.plot.bar(x='Date', y='Percent', color='red', ax = axes[0], title='data taken from Berliner Morgenpost - ' + dataFile +" (" + lastDate + ")"+ '\n\nNeuinfektionen in Prozent zur Gesamtzahl der Infizierten (akt. Wert: ' + lastPercent + ")")
    outValue.plot.bar(x='Date', y='Diff', color='blue', ax = axes[1], title='Unterschied zum Vortag (absolut) (akt. Wert: ' + lastDiff + ")")
    outValue.plot.bar(x='Date', y='DiffDiff', color='blue', ax = axes[2], title='Unterschiedsänderung zum Vortag (absolut) (akt. Wert: ' + lastDiffDiff + ")")
    plt.tight_layout()

    # save it in a file
    plt.savefig("Relative_Values_" + localSuffix + ".png", dpi=300)

    ##
    #fig, axes = plt.subplots(2,1)
     

    # subplots with full nd second with only last 30 day due to scaling
    fig, axes = plt.subplots(4,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False) 
    axes[2].xaxis.set_visible(False) 
    
    lastRelInfectedToLastWeek = f"{outValue.iloc[-1]['relInfectedToLastWeek']:.2f}"
    reproRate = f"{outValue.iloc[-1]['reproRate']:.2f}"
    
    outValue.plot.bar(x='Date', y='relInfectedToLastWeek', ax = axes[0] ,color='red', title='data taken from Berliner Morgenpost - ' + dataFile +" (" + lastDate + ")" +'\n\nRelativer Wert der Änderung zum Wert vor 5 Tagen (akt. Wert: ' + lastRelInfectedToLastWeek + ")")
    outValue.plot.bar(x='Date', y='relInfectedToLastWeek20', ax = axes[1] ,color='red', title='Relativer Wert der Änderung zum Wert vor 5 Tagen (letzte 20 Tageswerte) (akt. Wert: ' + lastRelInfectedToLastWeek + ")")
    outValue.plot.bar(x='Date', y='reproRate', ax = axes[2] ,color='blue', title='Reproduktionsrate Intervall 4 Tage (akt. Wert: ' + reproRate + ")")
    outValue.plot.bar(x='Date', y='reproRate20', ax = axes[3] ,color='blue', title='Reproduktionsrate Intervall 4 Tage (letzte 20 Tage)(akt. Wert: ' + reproRate + ")")
    plt.tight_layout()
    # save it in a file
    plt.savefig("Relative_Values_LastWeek" + localSuffix + ".png", dpi=300)

    # reprorates
    fig, axes = plt.subplots(4,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False) 
    axes[2].xaxis.set_visible(False) 
    
    reproRate = f"{outValue.iloc[-1]['reproRate']:.2f}"
    reproFlexRate = f"{outValue.iloc[-1]['reproFlexRate']:.2f}"
    outValue.plot.bar(x='Date', y='reproFlexRate', ax = axes[0] ,color='red', title='data taken from Berliner Morgenpost - ' + dataFile +" (" + lastDate + ")" +'\n\nReprorate ' + " (Interval: " + f"{flexInt} Tage) :" + reproFlexRate )
    outValue.plot.bar(x='Date', y='reproFlexRate20', ax = axes[1] ,color='red', title='Reproduktionsrate Intervall ' + f"{flexInt}" + ' Tage (letzte 20 Tageswerte)')
    outValue.plot.bar(x='Date', y='reproRate', ax = axes[2] ,color='blue', title='Reproduktionsrate Intervall 4 Tage (akt. Wert: ' + reproRate + ")")
    outValue.plot.bar(x='Date', y='reproRate20', ax = axes[3] ,color='blue', title='Reproduktionsrate Intervall 4 Tage (letzte 20 Tage)(akt. Wert: ' + reproRate + ")")
    plt.tight_layout()
    # save it in a file
    plt.savefig("Reprorate" + localSuffix + ".png", dpi=300)
    print(f"Suffix {localSuffix} done.")
    return



if __name__ == '__main__':
    jobs = []
    for localSuffix in localSuffixes:
        print(f"starting process for suffix {localSuffix}")
        # spawn the worker
        x = Process(target=processWorker, args=(localSuffix,))
        x.start()
        jobs.append(x)
    # all processes started
    for x in jobs:
        # wait for all jobs to close
        x.join()
    
