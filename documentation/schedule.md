### COG: checkup
### NAME: schedule

#### IMPORTANT:
This command does not update intern lists after a schedule is created.
This means that the `!updatecheckup` command must be used
if interns join the organization after the reminder schedule has been set.

This command also uses the 24 hour EST clock.

#### DESCRIPTION:
The bot has a feature that schedules the runcheck command. This
allows interns to get a reminder automatically.
This command can be used to set a schedule, remove a
schedule, or view all current schedules. A schedule is a
date and time that the bot will remind interns
to post updates.

#### USAGE:
- To get a list of current schedules:\
`!schedule show`

- To set a new schedule:\
`!schedule [day] [HH:MM]`

- To remove a schedule:\
`!schedule remove [index]`

- Example to make a new schedule for Friday at 6PM:\
`!schedule friday 18:00`

- Example to remove the first schedule
(schedule indexes are displayed with the 
'!schedule show' command):\
`!schedule remove 1`
