# CoronaCurve
Plot some Corona measures (because I did not find the KPIs of my personal interest)

I just wanted to know whether the number of corona new infected people goes up faster or slower than the last day. As I did not find it on any website, I decided to do it on my own. 

feel free to contribute to the project on [GitHub](https://github.com/jlinkohr/CoronaCurve) !

jochen.linkohr@gmx.de

## Here the results:

### update 5 April 2020: added Chart "last Week"
As I wanted to know if the shutdown has any impact on the infection rate and how much it is progressing, 
I added a new KPI "Relative LastWeek" which is the relation of new infected compared to the amount of 5 days before. I am assuming that someone who already has a documented infection will be separated and not infect new people (I know, this is a small error, but without knowing, I tried to simplyfy the model. )
### update 11 April 2020: added "last 20 days" to the above chart
The values are going down. To see how data changes, the scale is smll enough. So I added a chart only with the last 20 days to see how the values progressed in the last 2-4 infection cycles
### update 29 April 2020: added "reproRate" and "reproRate20" KPI
This value is the relation of the new infection of two blocks of data: the number of new infected people in a period of 8 day ago to 4 days ago. They might have infected people because they did not know that they are infected. The assumption is that the incubation time is approx 5 days. this sum if new infected people lead to the next block (today and the last three days). The relation of these blocks can be seen as the reproduction rate (the number of people one person infected). If the number is lower than one, the numbers will go down, if it is higher they will go up.  

### Germany total: 

[Absolute Values Germany](https://jlinkohr.github.io/CoronaCurve/Absolute_Values_GER.png)

[Relative Values Germany](https://jlinkohr.github.io/CoronaCurve/Relative_Values_GER.png)

look at the values on 21st of March: there you can see an immense decrease in the rate (which means the shutdown of schools and most companies 5 days ago has an effect. The shape of the curve repats 5 days later...). So it is proved that the shutdown had an effect ! If we restart, we should have a look on this value as well as the absolute values...

[Relative Infection rate to 5 day ago and reproduction rate Germany](https://jlinkohr.github.io/CoronaCurve/Relative_Values_LastWeekGER.png)

### Baden-Württemberg:

[Absolute Values Baden-Württemberg](https://jlinkohr.github.io/CoronaCurve/Absolute_Values_BW.png)

[Relative Values Baden-Württemberg](https://jlinkohr.github.io/CoronaCurve/Relative_Values_BW.png)

[Relative Infection rate to 5 day ago and reproduction rate Baden-Württemberg](https://jlinkohr.github.io/CoronaCurve/Relative_Values_LastWeekBW.png)

### Bayern:

[Absolute Values Bayern](https://jlinkohr.github.io/CoronaCurve/Absolute_Values_BY.png)

[Relative Values Bayern](https://jlinkohr.github.io/CoronaCurve/Relative_Values_BY.png)

[Relative Infection rate to 5 day ago and reproduction rate Bayern](https://jlinkohr.github.io/CoronaCurve/Relative_Values_LastWeekBY.png)
### World: 

[Absolute Values world](https://jlinkohr.github.io/CoronaCurve/Absolute_Values_WORLD.png)

[Relative Values world](https://jlinkohr.github.io/CoronaCurve/Relative_Values_WORLD.png)

[Relative Infection rate to 5 day ago and reproduction rate World](https://jlinkohr.github.io/CoronaCurve/Relative_Values_LastWeekWORLD.png)

### USA: 

as we see, the US rate is going down, but they will need one or two cycles before being really down

[Absolute Values USA](https://jlinkohr.github.io/CoronaCurve/Absolute_Values_US.png)

[Relative Values USA](https://jlinkohr.github.io/CoronaCurve/Relative_Values_US.png)

[Relative Infection rate to 5 day ago and reproduction rate US](https://jlinkohr.github.io/CoronaCurve/Relative_Values_LastWeekUS.png)

###### Data is taken from : https://interaktiv.morgenpost.de/corona-virus-karte-infektionen-deutschland-weltweit/


