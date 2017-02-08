
reminder_leads = ["remind me", "remember", "I need", "don't let me forget", "got to remember", "I need to remember", "reminder"]
reminder_heads = ["bring the lamp to my office", "bring the csa boxes", "pay the rent", "get groceries", "do the dishes", "feed the cat", 
					"call a dentist", "file taxes", "finish essay draft", "put away the laundry", "buy my wife a gift", "build Benedict"]
task_list_terms = ['my todo list', 'the todo list', 'my to do list', 'the to do list', 'to do list', 'do list', 'list', 'my list', 'the list', 'to dos', 'tasks', 'task list']

dows = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", ]
day_mods = ["this", "next", "every", "every other"]
times = ["morning", "afternoon", "evening", "night", "at 11 am", "at 3 p m", "at noon", "at 5 p m"]
datetimes = [dm + ' ' + d for d in dows for dm in day_mods]
datetimes += [d + ' ' + t for d in dows for t in times]
datetimes += dows
datetimes += ['tomorrow ' + t for t in times]
datetimes += ['tomorrow']
datetimes += [m + ' week' for m in day_mods]

def gen_reminders(output):
	for lead in reminder_leads:
		for head in reminder_heads:
			s1 = lead + ' to ' +  head
			output(s1)
			for dt in datetimes:
				s2 = s1 + ' ' + dt
				output(s2)

			for tail in task_list_terms:
				s3 = 'add ' + head + ' to ' + tail
				s4 = 'put ' + head + ' on ' + tail
				s5 = 'add to ' + tail + ' ' + head
				output(s3)
				output(s4)
				output(s5)

def gen_check_reminders(output):
	for term in task_list_terms:
		output('what is on ' + term)
	for w in ['do', 'remember', 'finish', 'accomplish', 'complete']:
		for dt in datetimes:
			output('what do I need to ' + w + ' ' + dt)
			output('what should I ' + w + ' ' + dt)
	output('what do I need to do')

def gen_calendar(output):
	heads = ['what is on', 'whats on']
	joins = ['my', 'the']
	nouns = ['calendar', 'schedule', 'agenda']

	for h in heads:
		for j in joins:
			for n in nouns:
				for dt in datetimes:
					output(h + ' ' + j + ' ' + n)
					output(h + ' ' + j + ' ' + n + ' ' + dt)
					output('what does ' + j + ' ' + n + ' look like')
					output('what does ' + j + ' ' + n + ' look like for ' + dt)

def gen_add_to_calendar(output):
	nouns = ['calendar', 'schedule', 'agenda']
	events = ['meeting', 'party', 'appointment', 'reservation', 'plans', 'class', 'lecture', 'section', 'seminar', 'colloquium', 'office hours', 'work', 'vacation', 'ski trip', 'dance competition']
	for ev in events:
		for n in nouns:
			output("add %s to my %s" % (ev, n))
			output("put %s on the %s" % (ev, n))
			for dt in datetimes:
				output("add %s to my %s at %s" % (ev, n, dt))
				output("put %s on the %s %s" % (ev, n, dt))
		for dt in datetimes:
			output("I have a %s %s" % (ev, dt))
			output("There's a %s %s" % (ev, dt))
			output("I'll be at a %s %s" % (ev, dt))

def gen_weather(output):
	phrases = ["is it gonna", "is it going to", "will it", "what is chance of", "chance of"]
	nouns = ["rain", "storm", "rainstorm", "shower", "showers", "drizzle", "pour", "downpour"]
	for dt in datetimes:
		for p in phrases:
			for n in nouns:
				output(p + ' ' + n)
				output(p + ' ' + n + ' ' + dt)

		conditions = ['rainy', 'sunny', 'cloudy', 'windy', 'foggy', 'hailing', 'dusty']
		for c in conditions:
			output('will it be ' + c)
			output('will it be ' + c + ' ' + dt)
			output('is it ' + c)
			output('is it ' + c + ' ' + dt)

	output('what is weather')
	output('what is the weather')
	output('what weather')
	output('weather')

if __name__ == "__main__":
	with open('training_data/add_calendar.txt', 'w') as f:
		output = lambda s: f.write(s + '\n')
		gen_add_to_calendar(output)


			