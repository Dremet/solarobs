# solarobs
Python library to quality-check, enhance and visualize your solar radiation observations.

The main idea is to provide a simple and easy-to-use python library for solar data analysts and to support the renewable energy sector.

## Features

1. Run preprocessing routines on your datasets such as applying time shifts or change the timestamp definitions – if necessary.
2. Run quality-checks to identify problems with your solar radiation measurements and correct them – if possible.
3. Fill gaps in your datasets – where possible/useful.
4. Visualize your data and the results of the quality-checks, the data itself and for additional manual quality-checks.

## Use it, if all of these apply:

- you have solar radiation measurement data recorded by ground measurement stations
- your data has a time resolution of 10 minutes or better (preferably 1 minute)
- you know how to read in your data into a pandas DataFrame
- you know your data / you have meta data
    - Which instruments have been used? What's their accuracy? What are caveats to consider when using them?
    - Were the devices properly installed? E.g. leveling is crucial and can significantly influence your measurements.
    - What about the maintenance and cleaning of the measurement stations? Regular cleaning is crucial. If your measurement station was not cleaned regularly, it might not be useful at all.

## Do not use this, if one of these apply:

- you want to process solar radiation measurement data recorded by satellites
- your data has a time resolution of less than 10 minutes
- you have never worked with pandas DataFrames
- you do not know your data / you have insufficient meta data


## Important Remarks

- This library only supports finding issues with your data. It **does not guarentee to find all issues**. Hence – as written above – you should study your meta data, know about the instruments used and the general framework of the measurement campaign (cleaning intervals, maintenance, professional installation, …).
- If not explicitely stated, all **functions expect data to be in UTC time zone**. If you have data in a local time zone, which is generally a bad idea, you need to change the timestamps.
- Make sure **your data is calibrated**.

## Timestamp Reference

One aspect many people ignore is to define which time interval a row in their dataset refers to. This is less important with better resolution, but one should be aware of this. There are basically four possibilites. If your dataset has a time resolution of 1 minute, your GHI (Global Horizontal Irradiation) value for 10:42 could refer to:
1. the mean value of all measurements between 6:41:01 and 6:42:00
2. the mean value of all measurements between 6:42:00 and 6:42:59
3. the mean value of all measurements between 6:41:30 and 6:42:29
4. the instantenous value at 6:42:00

The first three options are based on the assumption that data is collected every second, but only saved every minute to save disk space or mobile data usage. 

Option 1. is very common in meteorology as you wait for all measurements to come in and then log the data at the end of the minute.

Option 2. is uncommon and not recommended.

Option 3. actually makes a lot of sense, especially for solar measurements. If you want to use the solar position to calculate certain parameters and the time stamp refers to the middle of your averaging time period, the solar position will fit pretty well to the actual average sun position during that period. Besides that, it should just intuitively make sense to use the timestamp in the middle of the averaging period in terms of representativity.

Option 4 is the obvious choice, if your sample rate equals the time resolution of the data file.

This library expects data to be provided as in option 3, but at 1 minute time resolution this is not of high relevance.