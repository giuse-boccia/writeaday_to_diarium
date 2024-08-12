# Writeaday to Diarium

[Diarium](https://diariumapp.com/) gives you the option to import your entries from other apps such as Daylio or Evernote.
However, there is no option to import from [Writeaday](https://play.google.com/store/apps/details?id=com.compscieddy.writeaday).

## Usage

1. Open Writeaday, click the "All entries" button, then export all your entries to a .txt file.
2. Copy this .txt file to your PC
3. Run the Python script to convert it to .csv
4. Copy the .csv back to the device where you use Diarium
5. Open settings > Diary > Migrate from other app > Daylio and select the .csv from the previous step

## More info

To import entries from Writeaday into Diarium, one option is to convert the Writeaday export into the format of one of the supported apps. The easiest one is Daylio, which uses a simple CSV format.

I downloaded the Daylio app, created a couple of entries (containing also line breaks, commas and quotes) and then exported them to CSV:

```
full_date,date,weekday,time,mood,activities,note_title,note
2024-08-12,August 12,Monday,13:52,good,"","","Great note<br><br>such ""good"" note, really!<br><br>Make sure to include the \n, as well as a comma , and quotes "" because why not"
2024-02-12,February 12,Monday,13:53,meh,"","","Another note, this time in the past"
```

On the other hand, my Writeaday export to .txt looks like this:

```
01-29-2023
[7:03 PM] This is the first entry of the day.
[11:43 PM] This is another "entry", later in the day

01-30-2023
                [11:00 AM] This is an entry of the following day.
It is composed of multiple lines
```

A couple of things to be careful:

-   Writeaday keeps new lines in the .txt export, while Daylio uses `<br>`
-   Daylio also escapes quotes using a two double-quote characters
-   Writeaday uses a different date and time format and groups entries of the same day

Keeping those things in mind, I created a Python script that takes the name of the Writeaday .txt file and parses it
into Daylio's CSV export format.

I should be able to import this CSV into Diarium from Settings > Diary > Migrate from other app > Daylio
