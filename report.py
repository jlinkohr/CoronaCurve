import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import date

# process files with these suffixes
localSuffixes = ["BW", "BY", "GER"]

# date string for reports
today = date.today().strftime("%d.%m.%Y")


for localSuffix in localSuffixes:
    print (f"------ processing {localSuffix} -----\n")

    #set the filename to process
    dataFile = "coronaData_" + localSuffix + ".csv"

    # read the data
    total = pd.read_csv(dataFile)

    # calculate the difference of totals

    i = 0
    AktDiff = pd.DataFrame(columns=['Diff', 'Percent', 'DiffDiff'])
    lastDiff = 0

    # go through all values and calculate the addiional kpis for each day
    for x in range(len(total)):

        aktval=total.iloc[i]['Total']
        if (i != 0):
            lastval=total.iloc[i-1]['Total']
        else:
            lastval = 0
        i=i+1

        # calculate difference between last value and actual value
        diff=aktval-lastval

        # calculate percentage of change in relation to last value
        if (lastval != 0):
            percent=diff/lastval*100
        else:
            #if first value, set to zero
            percent=0

        # calculate difference of difference (2nd diff)
        DiffDiff = diff-lastDiff
        lastDiff = diff

        AktDiff = AktDiff.append({'Diff' : diff, 'Percent': percent, 'DiffDiff' : DiffDiff}, ignore_index=True)

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

    # ------------ first chart (containing of 3 subplots) ----------------
    fig, axes = plt.subplots(3,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False)

    # subchart 1: total
    outValue.plot(x='Date', y='Total', ax=axes[0], title='data taken from Berliner Morgenpost - ' + dataFile + " (" + today + ")" +'\n\nAnzahl Infizierte')
    axes[0].get_legend().remove()

    # subchart 2: curated
    outValue.plot(x='Date', y='Curated', color='green', ax=axes[1], title='Anzahl wieder gesund')
    axes[1].get_legend().remove()

    # subchart 3: deaths
    outValue.plot(x='Date', y='Deaths', color='red', ax=axes[2], title='Anzahl Tote')
    axes[2].get_legend().remove()
    # autofromat the layout to fit
    plt.tight_layout()
    # save it in a file 
    plt.savefig("Absolute_Values_" + localSuffix + ".png", dpi=300)

    # ------------ second chart (containing of 3 subplots): the calculated values -------------
    fig, axes = plt.subplots(3,1)
    axes[0].xaxis.set_visible(False) 
    axes[1].xaxis.set_visible(False)

    outValue.plot.bar(x='Date', y='Percent', color='red', ax = axes[0], title='data taken from Berliner Morgenpost - ' + dataFile +" (" + today + ")"+ '\n\nNeuinfektionen in Prozent zur Gesamtzahl der Infizierten')
    outValue.plot.bar(x='Date', y='Diff', color='blue', ax = axes[1], title='Unterschied zum Vortag (absolut)')
    outValue.plot.bar(x='Date', y='DiffDiff', color='blue', ax = axes[2], title='Unterschiedsänderung zum Vortag (absolut)')
    plt.tight_layout()

    # save it in a file
    plt.savefig("Relative_Values_" + localSuffix + ".png", dpi=300)
    
    # dont show, we are saving only, uncomment to see the chart instant
    # plt.show()
    # p = input()
