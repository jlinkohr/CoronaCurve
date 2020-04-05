import pandas as pd 
import matplotlib.pyplot as plt 

# process files with these suffixes
localSuffixes = ["BW", "BY", "GER", "WORLD", "US"]

for localSuffix in localSuffixes:
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

        i=i+1

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

        AktDiff = AktDiff.append({'StillInfected' : stillInfected, 'Diff' : diff, 'Percent': percent, 'DiffDiff' : DiffDiff}, ignore_index=True)

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
    
    # dont show, we are saving only, uncomment to see the chart instant
    # plt.show()
    # p = input()
