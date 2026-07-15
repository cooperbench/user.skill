> DEVELOPER

can we make the auxilio-extension row that we add in google calendar event more dynamic and reasonable, like when an event is saved with a location we nudge them if they want to send passes or room is added in the calendar we nudge them if they want to send passes, if an event is already linked to a invite pass, we show something like : Manage visitors Manage guests and send entry passes, and if its a new event with no linked invite passes we write something like Create Invite Passes , Subtitle : Send entry passes to visitors. You decide the suitable title and subtitle that makes sense to the user and make them want to use it. but keep them short. also we need to this reliably and fast.

> AGENT

I'll explore the auxilio-extension to understand the current implementation of the calendar event row/nudge before designing changes.

> AGENT

Now let me understand the background's data layer — what status info is available about an event (linked pass vs new), and how nudge targets are computed.

> AGENT

Let me read the sync layer and config to understand what marks an event and what status is locally available.