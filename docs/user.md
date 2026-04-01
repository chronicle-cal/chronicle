# User 

Chronicle is a web-based calendar app designed for calendar syncing, managing and smart scheduling.

# Features

- Connect multiple calendar sources (CalDAV, iCal)
- Aggregate events into one main calendar
- Organize calendars using profiles
- Smart scheduling: create tasks that will be scheduled and synced in your calendar

This guide explains how to:

- create profiles
- add calendars and sync them
- add tasks for smart scheduling

within Chronicle.

## Usage

### Sign in / Sign up

To use Chronicle, you need a user account (email and password). If you already have one just sign in.

### Create a calendar profile

A calendar profile is a container for your events and appointments. You can create multiple profiles (e.g. work, personal).

Each profile requires a main calendar. This is where all events and scheduled tasks will be stored.

The main calendar must support CalDAV.

> Important: Google Calendar and iCloud are currently not supported.

### Add calendar sources

You can connect external calendar sources (iCal or CalDAV) to your profile using the **Calendar Sources** feature. This way you can sync your events and appointments into your calendar profile. After adding your calendar sources, use `Sync Now` to push them to your main calendar.

You can get an overview of all added calendars and add additional, new sources in the **Calendars** tab. 

### Smart Scheduling

You can create tasks in Chronicle which support smart scheduling. This means that you can specify a task with a priority, a deadline and a duration and Chronicle will find free slots in your calendar and create appointments for you. After adding tasks, you need to synchronize them:

1. Click `Synchronize Now` to process tasks
2. Then go to `Manage` → `Sync Now` to push them to your calendar

After creating your profile, it will appear in the navigation bar where you can add tasks for your profile. 

Chronicle Events can be smart scheduled. So you can input something like:

- Work out, 3 times a week for one hour
- Study for the exam, every day for 2 hours, until the 30th of June

With this information Chronicle finds free slots, creates these appointments and syncs these with your connected calendars.

## Common Errors/Mistakes/Tips

- Make sure your main calendar supports CalDAV
- Always run `Sync Now` after adding tasks
- Check that your calendar sources are connected correctly

# Questions?

Feel free to open Issues if you have any questions.

