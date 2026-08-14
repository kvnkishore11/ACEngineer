# Multi-Team Agentic Coding

**Key:** `ma-2-lead-agents`

**Source:** YouTube (see meta)

---

**[00:00:00]** If you've been building with agents and

**[00:00:02]** pushing what you can do with your

**[00:00:04]** agentic coding tool, you've realized

**[00:00:06]** something critical. One agent is not

**[00:00:09]** enough. Imagine this. It's the end of

**[00:00:11]** 2026 and you've evolved your engineering

**[00:00:14]** from a single agent to multiple agents

**[00:00:17]** to agent teams. They've been building

**[00:00:20]** and learning just like you because you

**[00:00:22]** stopped using agents that forget and you

**[00:00:25]** started using agent experts. Each agent

**[00:00:29]** team you have contains agents that have

**[00:00:31]** their own skills, expertise, and domain

**[00:00:35]** knowledge, supercharging them so that

**[00:00:37]** they outperform any other agent. In

**[00:00:40]** fact, you have a few agent teams that

**[00:00:42]** are outperforming your co-workers.

**[00:00:44]** Engineers, one agent is not enough.

**[00:00:48]** Multi-agent orchestration and tools like

**[00:00:50]** Claude Code are the current frontier,

**[00:00:53]** but today I want to show you a system

**[00:00:55]** that pushes beyond Claude Code. This is

**[00:00:58]** multi-team agentic coding. Here we use

**[00:01:02]** specialized teams of agents to

**[00:01:05]** outperform the normal distribution of

**[00:01:07]** results. Now, if you're cost min-maxer

**[00:01:09]** and you care about saving money over

**[00:01:11]** getting results, this video is not for

**[00:01:13]** you. But, if you're an engineer working

**[00:01:15]** on mid- to large-size production code

**[00:01:17]** bases, stick around and let's take a

**[00:01:20]** peek at the performance gains you can

**[00:01:22]** get from multi-team agentic coding.

**[00:01:29]** Here we have a customized Pi coding

**[00:01:32]** agent. We've re-engineered the entire

**[00:01:35]** experience so that we're inside of a

**[00:01:37]** chat room with our teams of agents.

**[00:01:40]** Let's start out simple and then expose

**[00:01:42]** the valuable properties this system has.

**[00:01:44]** We'll start with my favorite, ping.

**[00:01:46]** We're talking to our orchestrator. It's

**[00:01:48]** giving us a classic ping-pong response.

**[00:01:50]** Let's talk to our team leads. Ping each

**[00:01:54]** team lead. Now, our orchestrator is

**[00:01:56]** going to call every team lead and you

**[00:01:59]** can see there our team leads are now

**[00:02:01]** responding. Notice here we have a

**[00:02:03]** two-layer architecture where we have an

**[00:02:06]** orchestrator talking to our team leads.

**[00:02:08]** All of our team leads responded and now

**[00:02:10]** our orchestrator is composing the

**[00:02:12]** results and giving us the final

**[00:02:14]** response. Of course, in the footer you

**[00:02:15]** can see all of our details. We have our

**[00:02:17]** orchestrator, leads, contacts, and total

**[00:02:20]** cost summed together. So the

**[00:02:21]** orchestrator cost here is the cost of

**[00:02:23]** the entire multi-team system. But this

**[00:02:26]** goes even deeper. As you saw here in the

**[00:02:28]** beginning, these are multiple teams of

**[00:02:32]** agents. Let me show you exactly what I

**[00:02:34]** mean. Have engineering and present tree

**[00:02:36]** structure of the most important files.

**[00:02:38]** And so we're delegating directly to our

**[00:02:40]** engineering team. So our engineering

**[00:02:42]** lead is going to take over. We're at

**[00:02:43]** mentioning them and now engineering is

**[00:02:45]** going to do something incredible. It's

**[00:02:46]** going to delegate to front-end

**[00:02:49]** developer. Our engineering lead tried to

**[00:02:51]** access files that it doesn't have

**[00:02:53]** permission to. It stepped out of its

**[00:02:55]** domain. And so it realized this and it

**[00:02:57]** delegated to its team members who have

**[00:02:59]** the right tools. So this might seem like

**[00:03:01]** an annoyance or like a waste of tokens,

**[00:03:04]** but it's actually very valuable. The

**[00:03:05]** engineering lead prompted the back-end

**[00:03:07]** developer and it also prompted the

**[00:03:09]** front-end developer for an answer. And

**[00:03:11]** so you can see both these agents getting

**[00:03:13]** work done here in a chat-like interface.

**[00:03:16]** And so what we have here is three tiers

**[00:03:19]** of agents. We have our orchestrator, we

**[00:03:21]** have our leads, and we have our workers.

**[00:03:24]** They both responded to the lead and now

**[00:03:26]** the lead is going to respond to the

**[00:03:28]** orchestrator. This is a very very

**[00:03:30]** powerful multi-team orchestration tool.

**[00:03:33]** There it is, engineering nailed it.

**[00:03:34]** Here's the rundown. And now our

**[00:03:35]** orchestrator is giving us a full

**[00:03:37]** breakdown of what's going on. This

**[00:03:39]** multi-team tool has advantages already

**[00:03:43]** over the normal prompting back-and-forth

**[00:03:45]** experience. If we hit {slash} toggle

**[00:03:48]** workers, we can see our actual full team

**[00:03:51]** breakdown. We've been conversing with

**[00:03:53]** our engineering team, and engineering

**[00:03:55]** team has looked up files, it's read its

**[00:03:57]** context, and it's done something

**[00:03:59]** incredible as well. If you realize here

**[00:04:00]** that out of the box for a simple command

**[00:04:03]** like that, the context is actually quite

**[00:04:05]** high. You've noticed something really

**[00:04:06]** important about this system. Our agents

**[00:04:08]** are loading memory files. They're

**[00:04:10]** loading their agent expertise. More on

**[00:04:12]** that in a moment. If you can see how

**[00:04:14]** powerful this system can be, definitely

**[00:04:16]** like, subscribe so you let the algorithm

**[00:04:18]** know that you're interested in

**[00:04:19]** multi-agent orchestration like this.

**[00:04:21]** Let's keep pushing this system further.

**[00:04:23]** We're operating in a prompt routing code

**[00:04:25]** base. And I can blow up the code base

**[00:04:27]** here. It's a common problem a lot of

**[00:04:28]** LLM-based applications have. You don't

**[00:04:30]** want to pay for intelligence that you

**[00:04:32]** don't need. Specifically, when you have

**[00:04:33]** thousands and thousands of users running

**[00:04:35]** your application that hits agents or

**[00:04:37]** hits some LLM at some point, your simple

**[00:04:39]** prompts don't need to hit expensive

**[00:04:41]** models. For example, you don't want Opus

**[00:04:43]** 4.6 to run with high reasoning when you

**[00:04:46]** can just have Claude Haiku respond or

**[00:04:48]** Sonnet respond. There's a great

**[00:04:49]** breakdown of a highly intelligent model,

**[00:04:51]** a medium intelligent model, and a

**[00:04:54]** not-so-intelligent but very cheap model.

**[00:04:56]** And we can go even cheaper than this. Of

**[00:04:58]** course, there are cheaper, frankly

**[00:04:59]** better models than Haiku, but just as an

**[00:05:01]** example, this is a common problem you're

**[00:05:03]** going to want to solve when building

**[00:05:05]** with LLMs. You don't want to pay for

**[00:05:07]** intelligence that you don't need. So,

**[00:05:09]** what we have here is a prompt complexity

**[00:05:11]** classifier. It's very simple, and we can

**[00:05:13]** run it right now. So, you know, if we

**[00:05:15]** open up a terminal inside this code

**[00:05:16]** base, and we type J for just, we're of

**[00:05:18]** course using just file for quick

**[00:05:20]** commands, and J is an alias for just

**[00:05:22]** just to be super clear. We can do just

**[00:05:24]** predict summarize this code base. And

**[00:05:27]** now our system should predict that only

**[00:05:29]** a medium or a low-tier model is needed

**[00:05:32]** to satisfy this prompt. And we hit enter

**[00:05:34]** here, you can see our classifier

**[00:05:35]** running, and you can see our label is

**[00:05:38]** medium. There's all the confidences out

**[00:05:40]** of 100 or 100%. This type of prompt

**[00:05:43]** would route to Claude Sonnet 4.6 or

**[00:05:45]** whatever your medium-tier model is set

**[00:05:47]** to. So, that's the problem and that's

**[00:05:49]** what this code base is. But of course,

**[00:05:50]** we're not building this. We are having

**[00:05:52]** our agents and we're teaching our agents

**[00:05:54]** how to build it. And in this case, we

**[00:05:56]** actually have an entire agent team that

**[00:05:58]** knows how to run this code base better

**[00:06:00]** than anyone. At a previous job, I was a

**[00:06:01]** lead data scientist and I would spend a

**[00:06:03]** lot of time building out these

**[00:06:05]** classifier models by hand. Now, we can

**[00:06:07]** just have agents do it for us. So, I

**[00:06:09]** want to showcase one of the advantages

**[00:06:11]** of having teams that you work with

**[00:06:13]** instead of just individual agents,

**[00:06:15]** especially individual one-off agents.

**[00:06:17]** So, let's go ahead and ask our teams a

**[00:06:19]** question. What we're going to get here

**[00:06:21]** is a multi-perspective

**[00:06:22]** answer. So, I'll say, "Ask all teams,

**[00:06:25]** what are two additional scikit-learn

**[00:06:27]** classifiers we can test our current

**[00:06:30]** classifier against?" And so, once again,

**[00:06:32]** we're entering that chat pattern, always

**[00:06:34]** only talking to our orchestrator. And

**[00:06:36]** then our orchestrator decides who it

**[00:06:38]** needs to delegate the work to. I asked a

**[00:06:40]** question, it thought, it's delegating

**[00:06:41]** work out to its individual teams. You

**[00:06:44]** can see that it wrote the exact same

**[00:06:45]** prompt to every single team. It's very

**[00:06:47]** important, it's very consistent, and

**[00:06:49]** we'll showcase how it's able to do that

**[00:06:51]** in a moment. The individual team leads

**[00:06:53]** have taken over. So, we have our

**[00:06:54]** planner, we have our engineer, and we

**[00:06:55]** have our validator. It's completely up

**[00:06:57]** to them whether they decide to delegate

**[00:06:59]** additional work. It looks like the

**[00:07:00]** engineering lead is delegating work to

**[00:07:02]** the back-end dev. Our validation lead

**[00:07:04]** here has delegated to the security

**[00:07:06]** reviewer. QA engineer is there. You can

**[00:07:08]** see all the tools that's running.

**[00:07:10]** Planning lead is running, so on and so

**[00:07:12]** forth. And so, these are all going to

**[00:07:13]** run and put together all the results.

**[00:07:15]** And you can see all the work that each

**[00:07:16]** team is doing. You can see the costs and

**[00:07:18]** whatnot taking up. And now they're going

**[00:07:20]** to start to compose back their results.

**[00:07:21]** So, the flow here is orchestrator talks

**[00:07:24]** to the leads, leads talk to the workers.

**[00:07:26]** And then we get one unified response. We

**[00:07:28]** are conversing with our orchestrator and

**[00:07:31]** no one else. So, this is super, super

**[00:07:32]** important. Let me point something out

**[00:07:33]** here. All three teams weighed in,

**[00:07:35]** there's strong consensus. This is what

**[00:07:37]** you want to see. Linear SVC, calibrated

**[00:07:39]** classifier CV, unanimous pick across all

**[00:07:42]** teams. Digging in further, split

**[00:07:44]** recommendation. They both favor Claude

**[00:07:46]** man and B. Engineering prefers SGD

**[00:07:48]** classifier and then everyone agreed to

**[00:07:50]** skip certain things. This is a chat

**[00:07:52]** experience. And so one of the key

**[00:07:55]** elements of that is that every agent can

**[00:07:57]** see the conversation. Not to get too

**[00:07:59]** ahead of things here, but if I copy the

**[00:08:01]** session ID and I just search for this

**[00:08:03]** and I go to the conversation, you can

**[00:08:04]** see the entire conversation that's

**[00:08:06]** happened so far. In a JSON L file, you

**[00:08:09]** can see all of the leads and you can see

**[00:08:10]** the depths. I point this out just to say

**[00:08:12]** that every agent is aware of the

**[00:08:14]** conversation happening. And then our

**[00:08:16]** orchestrator starting to guide the

**[00:08:18]** experience. Want me to have engineering

**[00:08:19]** draft implementation for the benchmark.

**[00:08:21]** Let's go ahead and have our team build

**[00:08:22]** this out and I want to utilize the team

**[00:08:25]** structure that we've built here to get

**[00:08:27]** better results. So how can we do that?

**[00:08:29]** Let's do this. I'll say plan, engineer,

**[00:08:31]** and then validate. Make sure to add just

**[00:08:34]** commands to test both models and we'll

**[00:08:37]** call it, you know, just prompt both. All

**[00:08:39]** right, and then we'll fire that off. So

**[00:08:41]** plan, engineer, and then validate. Our

**[00:08:43]** orchestrator agent is going to write out

**[00:08:44]** a great detailed plan and then our lead

**[00:08:47]** is going to dive into things. So you'll

**[00:08:49]** notice here, really interesting thing

**[00:08:50]** that my plan lead does, it first always

**[00:08:53]** gets all the context. We are not afraid

**[00:08:56]** to spend to win here. We're not afraid

**[00:08:58]** to give our agents all the relevant

**[00:09:00]** context they need. And this is something

**[00:09:01]** critical we talked about in our previous

**[00:09:03]** week's video, the CEO agents. We talked

**[00:09:05]** about that key idea of giving your

**[00:09:07]** agents more context. Use that powerful 1

**[00:09:10]** million context window model inside of

**[00:09:12]** your Opus and your Sonic models so that

**[00:09:14]** they have all the information they need

**[00:09:16]** to succeed. This is a massive advantage

**[00:09:18]** you can be building into now as long as

**[00:09:20]** you're not afraid to spend to get the

**[00:09:22]** advantage. Something else important here

**[00:09:24]** to mention is why am I building and

**[00:09:26]** sharing a system like this with you? You

**[00:09:27]** always want to be thinking about where

**[00:09:29]** the ball is going, not where it is. We

**[00:09:32]** have a couple converging trends that are

**[00:09:34]** super super important that this

**[00:09:35]** application embodies. All right, we have

**[00:09:37]** incredible intelligence with increasing

**[00:09:40]** context windows. All right, we have the

**[00:09:41]** new 1 million context window here from

**[00:09:43]** Claude. This is very, very powerful and

**[00:09:45]** it unlocks a new frontier of what is

**[00:09:47]** possible. And then as you'll see here in

**[00:09:48]** a moment, we can specialize our agents

**[00:09:50]** even further by making them agent

**[00:09:53]** experts. And then we've scaled that idea

**[00:09:55]** thanks to a customizable agent coding

**[00:09:58]** tool. We are using the Pi agent harness

**[00:10:00]** to customize this entire experience. So

**[00:10:03]** we have powerful context windows. We

**[00:10:05]** have agents that learn. Let me be super

**[00:10:08]** clear about this. As you'll see, every

**[00:10:09]** one of these agents they have a working

**[00:10:11]** mental model about how things work and

**[00:10:13]** this grows over time. Every time you run

**[00:10:16]** your team, they're all taking notes,

**[00:10:18]** they're all building up their mental

**[00:10:19]** model and then they're loading it at the

**[00:10:20]** beginning. As you can see here, a lot of

**[00:10:22]** read tools happen in the beginning. The

**[00:10:24]** the book here represents the read tool

**[00:10:26]** calls and that's because they're always

**[00:10:28]** loading the conversation and their own

**[00:10:30]** specialized mental model. So we have

**[00:10:32]** large context windows coming in at

**[00:10:34]** cheaper costs. You're going to have so

**[00:10:36]** many tokens available to you. The

**[00:10:37]** question is are you using them? Then we

**[00:10:39]** have agent expertise. Thanks to the

**[00:10:40]** context window, you can really load up

**[00:10:43]** the specialization and the memory of

**[00:10:45]** every single specialized agent. And then

**[00:10:48]** of course, we have the Pi coding agent,

**[00:10:49]** the agent harness. You can build

**[00:10:51]** customized agentic experiences, not just

**[00:10:54]** agents, not just teams of agents, but

**[00:10:56]** the entire agent harness can be

**[00:10:57]** customized when you're using a tool like

**[00:11:00]** Pi. So I hope you can see, when you

**[00:11:01]** stack these things together, we're

**[00:11:03]** getting far away from the normal

**[00:11:04]** distribution of results.

**[00:11:11]** It all starts with the dot Pi file.

**[00:11:13]** Unlike dot Claude where you have agents,

**[00:11:16]** prompts, skills, so on and so forth,

**[00:11:18]** when you're customizing the agent

**[00:11:19]** harness, as we mentioned in last week's

**[00:11:21]** video, CEO agents, I'll link that in the

**[00:11:23]** description for you, you can customize

**[00:11:25]** the experience down to the folders, down

**[00:11:27]** to the individual files. Everything is

**[00:11:29]** customizable here. With that, we've

**[00:11:31]** customized the experience to look like

**[00:11:32]** this. We have a multi-team config. I

**[00:11:35]** really like this configuration-based

**[00:11:37]** approach because it means at any point

**[00:11:38]** in time, we can just copy our config,

**[00:11:40]** change up the teams, and specialize how

**[00:11:42]** we need. We have our orchestrator. We're

**[00:11:44]** passing in a path to the system prompt

**[00:11:47]** of the orchestrator. We'll break that

**[00:11:48]** down in a moment. And we have individual

**[00:11:50]** teams. If we jump into planning, we have

**[00:11:52]** our lead specified. It's just a system

**[00:11:54]** prompt and a name. All right. Then we

**[00:11:56]** have a couple additional properties,

**[00:11:57]** just a team color. And then we have the

**[00:11:59]** members. And we're repeating the

**[00:12:00]** pattern. We're giving the path to the

**[00:12:02]** system prompt of the agent. And this

**[00:12:04]** pattern is going to repeat for

**[00:12:05]** engineering. You can see there's the

**[00:12:06]** engineering team, front end, back end,

**[00:12:08]** that I've just copied the kind of

**[00:12:10]** default template. Um we don't need a

**[00:12:12]** front end dev for prompt routing. This

**[00:12:14]** is a data science back end focused type

**[00:12:16]** of code base. But nonetheless, we have a

**[00:12:18]** front end dev there. We can get rid of

**[00:12:19]** that. We can change that whenever we

**[00:12:20]** want. The three key nodes of building

**[00:12:22]** software, planning, engineering, and

**[00:12:25]** validation. So the pattern repeats. Nice

**[00:12:27]** and simple. The whole idea here is I'm

**[00:12:29]** setting up reusable, customizable

**[00:12:31]** systems that are easy to change and

**[00:12:33]** update. That's the configuration file

**[00:12:34]** that puts all the teams together. And

**[00:12:36]** you can see here we have a couple of key

**[00:12:37]** paths, where the agents are, where the

**[00:12:39]** sessions are, and where some of the logs

**[00:12:41]** are. Let's go ahead and open up that

**[00:12:42]** orchestrator, right? What does our

**[00:12:43]** orchestrator look like inside the

**[00:12:45]** system? We have our name, our model. Of

**[00:12:48]** course, for the orchestrator, we want to

**[00:12:49]** use the best intelligence available so

**[00:12:51]** that it coordinates everything properly.

**[00:12:53]** And then here we start deviating from

**[00:12:55]** the normal out-of-the-box AI coding

**[00:12:57]** experience you're probably used to. We

**[00:12:59]** have expert tees. Our orchestrator has a

**[00:13:02]** mental model of everything that's

**[00:13:03]** happened. It has complete control over

**[00:13:05]** it, so it's updatable. And we have max

**[00:13:07]** lines. We don't want this to grow too

**[00:13:08]** big. Frankly, with a million contacts

**[00:13:10]** available, this could be much larger,

**[00:13:12]** but 10,000 lines is still a ton of

**[00:13:14]** context. Here we have skills. You're

**[00:13:16]** likely used to this. The interesting

**[00:13:18]** thing here is that, let's say we open up

**[00:13:19]** our engineering lead. Our engineering

**[00:13:21]** lead also has zero micromanagement. So

**[00:13:24]** you can You the zero micromanagement

**[00:13:26]** skill is shared between the orchestrator

**[00:13:28]** and all the leads. The whole idea is

**[00:13:30]** don't micromanage, delegate the right

**[00:13:32]** work at the right time to the workers.

**[00:13:34]** And for the orchestrator, delegate the

**[00:13:36]** right work to the individual teams.

**[00:13:38]** Okay, so this is very powerful. We are

**[00:13:39]** sharing skills when necessary. You can

**[00:13:42]** see here we also have a conversational

**[00:13:44]** response skill, and this is shared

**[00:13:45]** between every other agent. If we open up

**[00:13:47]** our back-end agent here, it does not

**[00:13:50]** have that conversational response skill

**[00:13:52]** because we want our back-end dev, we

**[00:13:54]** want our developers, we want our

**[00:13:55]** builders to be very, very verbose and

**[00:13:58]** very detail-oriented. But when we get to

**[00:14:00]** our leads and our orchestrator, we don't

**[00:14:01]** really need that. We have the tools

**[00:14:03]** block here, and you can see the special

**[00:14:04]** skill that our orchestrator has is the

**[00:14:07]** delegate, and our lead also has

**[00:14:09]** delegate. Because remember this is a

**[00:14:11]** three-tier architecture. We have an

**[00:14:13]** orchestrator, leads, and workers. And

**[00:14:15]** then here comes something really

**[00:14:16]** powerful. We have domain. So this

**[00:14:18]** specifies what the agents can and cannot

**[00:14:20]** do and where they can and cannot go. And

**[00:14:22]** if you're working in a large code base,

**[00:14:24]** this is very, very powerful. Let's look

**[00:14:26]** at our planning lead. They have read

**[00:14:28]** access to everything. Here's that dot

**[00:14:30]** path. Read update access to the dot pi

**[00:14:32]** directory where they can, you know, look

**[00:14:34]** at and write their expertise. They also

**[00:14:37]** have full read access to the specs

**[00:14:38]** directory, right, where plans are

**[00:14:40]** actually written. But they can't update

**[00:14:43]** it. They must delegate that work. As you

**[00:14:45]** can see here, zero micromanagement.

**[00:14:47]** Always use this. You're a leader,

**[00:14:49]** delegate, never execute. So the leaders

**[00:14:52]** aren't actually doing any raw file

**[00:14:54]** changing-related work unless it's

**[00:14:56]** related to their mental model, which is

**[00:14:58]** stored in the expertise directory. So

**[00:15:01]** this is powerful. Think about what you

**[00:15:02]** can do with this. If you're operating a

**[00:15:04]** large, large code base, we're talking

**[00:15:05]** thousands of files, you can build

**[00:15:07]** specific agents that operate specific

**[00:15:10]** parts of the code base. This is a simple

**[00:15:13]** example, but my planners, they can read

**[00:15:15]** the entire code base, but they can't

**[00:15:16]** change anything. I don't want them to

**[00:15:18]** change anything. I want them to create

**[00:15:19]** plans. And so we have this enforced. You

**[00:15:22]** can imagine this dials right into the

**[00:15:23]** pie hooks system. If you're building out

**[00:15:25]** something like this with Claude,

**[00:15:27]** although you'll be a lot more limited in

**[00:15:28]** what you can do, you could also plug

**[00:15:30]** into the Claude code hooks capability.

**[00:15:32]** Pie has the exact same system. You have

**[00:15:33]** a bunch of hooks you can tap into. We

**[00:15:35]** detailed this in our pie versus Claude

**[00:15:37]** code video. Link in the description, of

**[00:15:39]** course. A very specialized experience.

**[00:15:41]** This front matter is custom built. We're

**[00:15:44]** building teams and we're building agents

**[00:15:46]** that do a couple things, right? So, it

**[00:15:47]** has expertise. These agents remember.

**[00:15:50]** Every time this agent boots up, it's

**[00:15:51]** going to load from its expertise file.

**[00:15:54]** And so, if we hop back to our system,

**[00:15:56]** let's see what's going on here. QA

**[00:15:58]** engineer is running. Our validation lead

**[00:16:00]** is looking at some stuff. And the

**[00:16:02]** validation is kicking off. Security

**[00:16:04]** reviewer. Security reviewer says ship

**[00:16:05]** it, no issues. But we can see here our

**[00:16:07]** QA engineer has found a couple things.

**[00:16:09]** And so, super important. We have

**[00:16:11]** multiple agents working on these teams.

**[00:16:13]** And they're going to find different

**[00:16:14]** things. They all have different context

**[00:16:16]** windows, different perspectives. And if

**[00:16:18]** we wanted to, they could all be running

**[00:16:19]** different models. So, it looks like the

**[00:16:21]** QA engineer has some information that

**[00:16:23]** the security validator doesn't. And if

**[00:16:25]** we scroll down here, the full life cycle

**[00:16:27]** is complete. And the orchestrator has

**[00:16:29]** put together the results of the system

**[00:16:31]** and communicated to us. To be super

**[00:16:34]** clear here, it is running all of these

**[00:16:36]** skills that it has, right? The

**[00:16:37]** orchestrator knows not to just give me a

**[00:16:39]** giant block of text back because it has

**[00:16:41]** the conversational response skill always

**[00:16:44]** used when writing responses. And so, our

**[00:16:46]** agent give us a nice, you know,

**[00:16:47]** relatively concise summary here. And now

**[00:16:49]** we have the next step, of course. But we

**[00:16:51]** had a whole team run through this

**[00:16:52]** workflow, planning, engineering, and

**[00:16:54]** validating. And so, very, very powerful

**[00:16:56]** stuff, right? 18 minutes so far, lots of

**[00:16:58]** work done. And now we can run train

**[00:17:00]** both, we can run prompt both. So, we can

**[00:17:02]** see how our classifiers are working now.

**[00:17:08]** New terminal window here. J. You can see

**[00:17:11]** we have those new methods that are

**[00:17:12]** multi-team agent coding tool built.

**[00:17:15]** Summarize this code base. Predict both.

**[00:17:17]** There you go. And you can see the kind

**[00:17:18]** of difference between them. They both

**[00:17:19]** are routing to mid, which is good. They

**[00:17:21]** agree on this. And then we can see some

**[00:17:23]** individual stats from our individual

**[00:17:25]** scikit-learn models, right? So, very

**[00:17:26]** powerful stuff. We can go ahead and test

**[00:17:28]** another prompt to see how they both

**[00:17:29]** perform. And what we really want is to

**[00:17:31]** probably run this eval. Do you want to

**[00:17:33]** run head-to-head eval on the holdout

**[00:17:34]** data set? So, let's just go ahead and do

**[00:17:36]** that. Run head-to-head.

**[00:17:38]** Again, we're going to see the power of

**[00:17:40]** locking the domain. Our orchestrator

**[00:17:42]** can't actually do this work. It knows

**[00:17:44]** that. So, it's delegating to

**[00:17:45]** engineering. And so, the lead, again,

**[00:17:47]** lead cannot do work. It is a thinker.

**[00:17:50]** It's a planner. It's a coordinator. And

**[00:17:52]** so, the lead passed that to back end.

**[00:17:54]** It's going to read what we have, and

**[00:17:56]** then it's going to run them

**[00:17:56]** head-to-head. We'll go ahead and let

**[00:17:57]** that run and come back to the results in

**[00:17:59]** a moment. And the way that you're

**[00:18:00]** building your agent to coding system is

**[00:18:02]** the edge now. And as I talk about all

**[00:18:04]** the time on the channel, we want to

**[00:18:05]** increase the trust we have in our

**[00:18:06]** agents. And in order to do that, we need

**[00:18:08]** specialized experiences. And And we want

**[00:18:10]** to dial things down to the agent

**[00:18:12]** harness. How can you build customized

**[00:18:14]** specialized systems that outperform, you

**[00:18:16]** know, normal distribution of results

**[00:18:18]** everyone else is getting? A great way to

**[00:18:20]** do that is to really know how to control

**[00:18:22]** the core four, context model, prompt,

**[00:18:24]** tools, and then orchestrate, right?

**[00:18:26]** Scale it. Below here is just a mostly

**[00:18:30]** standard system prompt with a couple of

**[00:18:32]** key differences. This is the

**[00:18:33]** orchestrator system prompt. I am

**[00:18:35]** injecting some variables at runtime

**[00:18:37]** before the agent loads the system

**[00:18:39]** prompt. Right, we have the session

**[00:18:40]** directory, we have the conversation log,

**[00:18:42]** and then we have the teams. So, the

**[00:18:44]** teams is coming dynamically in from our

**[00:18:46]** YAML file. We have its individual tools,

**[00:18:48]** and then I'm also giving the file paths,

**[00:18:51]** right? I'm actually loading in the

**[00:18:52]** expertise and skills block, right? I'm

**[00:18:54]** taking it out of the front matter, and

**[00:18:55]** I'm placing it inside the system prompt

**[00:18:57]** for the agent. Our orchestrator is

**[00:18:59]** acutely aware of all the skills it has,

**[00:19:01]** you know, it knows how to write mental

**[00:19:02]** models. You can see I have a mental

**[00:19:04]** model skill for tracking and keeping its

**[00:19:07]** mental model updated, as well as other

**[00:19:09]** things, right? For instance, I have an

**[00:19:11]** active listener skill. This is something

**[00:19:12]** that you just might not want. You might

**[00:19:14]** not want your agent to always read the

**[00:19:16]** conversation log before every response.

**[00:19:18]** But, this is something that I do want in

**[00:19:20]** my orchestrator. And in fact, if you

**[00:19:21]** just search this, you can see that I

**[00:19:23]** have this inside of every team member.

**[00:19:25]** Every single team member is And let me

**[00:19:27]** just dial this into this one path here,

**[00:19:29]** multi-team and agents. You can see we

**[00:19:31]** have our 10 agents all specialized. And

**[00:19:33]** they're all active listeners. Read the

**[00:19:36]** conversation log before every response.

**[00:19:37]** And so, by composing skills like this,

**[00:19:40]** we're able to control and quickly modify

**[00:19:42]** the capabilities of every single agent

**[00:19:45]** because often times there's shared

**[00:19:46]** capability you want. There could be an

**[00:19:48]** agent somewhere that we don't want to

**[00:19:50]** always active listen. We want it to be

**[00:19:52]** independent and not to rely on the

**[00:19:54]** current conversation. Easily changeable,

**[00:19:56]** modifiable from this multi-team agent

**[00:19:58]** architecture tool. This is how the

**[00:20:00]** system is kind of composed. Of course,

**[00:20:02]** we have a dot skills directory. Nothing

**[00:20:04]** really new here. Every one of these

**[00:20:05]** skills is modifiable. You can see

**[00:20:07]** everything we have there. Some are

**[00:20:09]** shared, some are not. We can jump into

**[00:20:11]** this. It's a classic prompt

**[00:20:12]** architecture. Nothing really huge to

**[00:20:14]** note here, but you can see here this is

**[00:20:16]** how agents are keeping track of their

**[00:20:17]** mental models. Instructions, personal

**[00:20:20]** expertise file, when to read, when to

**[00:20:21]** update, how to structure, you know, an

**[00:20:24]** improvement that can be made, a

**[00:20:25]** customization, a specialization you can

**[00:20:28]** make to your agents is teaching them

**[00:20:30]** exactly how you want them to write their

**[00:20:32]** mental models and to keep track of this.

**[00:20:34]** You want to be kind of careful here,

**[00:20:35]** though. When you're building agent

**[00:20:36]** experts, you don't want to be over rigid

**[00:20:38]** about this. Our agents are storing and

**[00:20:40]** maintaining their own mental models.

**[00:20:42]** They're storing what they think is most

**[00:20:44]** relevant to their success, and it's

**[00:20:46]** going to grow over each session. Again,

**[00:20:48]** when we talk about advantages over other

**[00:20:50]** systems, every time I boot this up, my

**[00:20:53]** agent teams, down to the individual

**[00:20:55]** workers, is going to have a stacking,

**[00:20:58]** compounding set of memory that's

**[00:21:00]** allowing them to specialize further and

**[00:21:02]** further and further over and over and

**[00:21:04]** over. And so, if you're building

**[00:21:05]** legitimate production software, this

**[00:21:07]** becomes very important to always go

**[00:21:09]** through your team because your team is

**[00:21:12]** the one accumulating knowledge. This is

**[00:21:14]** where domain specifying becomes really,

**[00:21:17]** really important. For example, like

**[00:21:18]** front-end dev, you might have something

**[00:21:20]** like this. And of course, your front-end

**[00:21:22]** dev can do whatever they need to here.

**[00:21:24]** So, you might have this and you'll

**[00:21:26]** probably also want them to be able to

**[00:21:27]** read the back-end, but never touch it.

**[00:21:30]** They can't actually touch this ever. One

**[00:21:32]** example there, and of course, we might

**[00:21:33]** want the exact opposite thing inside of

**[00:21:36]** our back-end dev. So, we could paste

**[00:21:37]** this and then we go back-end and we fix

**[00:21:40]** this. And now our back-end engineer and

**[00:21:43]** our front-end engineer sit next to each

**[00:21:45]** other. We can look at these side by side

**[00:21:46]** here, and this means that our agents can

**[00:21:49]** both read any file that they need to,

**[00:21:51]** but our front-end can only update and

**[00:21:53]** write to the front-end directory,

**[00:21:55]** whereas our back-end can only write and

**[00:21:57]** update and delete from our back-end

**[00:21:59]** directory. Over time, the specialization

**[00:22:01]** becomes more and more important as each

**[00:22:03]** member is building up their own mental

**[00:22:05]** model of the system. And thanks to the

**[00:22:07]** powerful new Claude 1 million true

**[00:22:10]** context windows, having expertise like

**[00:22:12]** this is more viable than ever. If we hop

**[00:22:14]** into the mental model for our back-end

**[00:22:17]** developer, it's actually got information

**[00:22:19]** stored about its previous codebase that

**[00:22:22]** I had it operating in. So, it's

**[00:22:24]** remembering all this. I actually need to

**[00:22:25]** get rid of this and tune the mental

**[00:22:27]** model, but this is an application that

**[00:22:28]** is tracking in its mental model. Its

**[00:22:30]** mental model is 5,000 tokens, and this

**[00:22:32]** is very powerful. Last export, there's a

**[00:22:33]** session, and it's just keeping track of

**[00:22:36]** not detailed specific information, just

**[00:22:38]** high-level information about what's

**[00:22:40]** going on. It's right between the specs,

**[00:22:42]** missing infrastructure, key risks,

**[00:22:44]** back-end patterns it noticed, security

**[00:22:46]** stuff, testing, so on and so forth. And

**[00:22:47]** so, it's just maintaining this on its

**[00:22:50]** own. I don't do anything with this. I

**[00:22:51]** don't touch this, and that's uh one of

**[00:22:53]** the key ideas with the mental model. You

**[00:22:55]** can't have your fingers on everything.

**[00:22:57]** And this is, you know, the journey that

**[00:22:59]** every engineer needs to make as they

**[00:23:01]** move toward becoming an agentic

**[00:23:02]** engineer. You have to let go. You have

**[00:23:04]** to teach your agents to operate as you

**[00:23:06]** would. The mental model is one of the

**[00:23:08]** greatest examples of this. You can give

**[00:23:10]** guidelines on how they should be

**[00:23:12]** building great mental models. We have

**[00:23:14]** that in our mental model skill, but

**[00:23:16]** we're not going much further than that,

**[00:23:18]** right? This skill is only 77 lines long

**[00:23:20]** and we're letting them maintain and

**[00:23:22]** update this on their own. That's

**[00:23:24]** expertise. That's our specialized

**[00:23:26]** agents. This is the system prompt that's

**[00:23:28]** loading into every single agent. We have

**[00:23:30]** skills, we have our configuration file,

**[00:23:32]** and we also have sessions. So, this is a

**[00:23:34]** really important idea. Let's go ahead

**[00:23:35]** and pull the session ID on this agent

**[00:23:37]** and just pull up the conversation log

**[00:23:39]** like we had before. You can see here

**[00:23:40]** we're also storing all of the tool calls

**[00:23:43]** for every single team. We're also

**[00:23:45]** storing the starting system prompt just

**[00:23:47]** so it's super, super clear. We can jump

**[00:23:49]** into our back-end dev here and we can

**[00:23:51]** see exactly what its system prompt looks

**[00:23:54]** like with everything templated in. Full

**[00:23:56]** control. You can see super, super

**[00:23:57]** simple, super concise. By placing this

**[00:23:59]** information in the system prompt, it is

**[00:24:01]** strongly adhering to this information.

**[00:24:03]** We are really detailing and controlling

**[00:24:06]** the core four down to the system prompt

**[00:24:08]** level. This is complete customization.

**[00:24:10]** If we hop back to our results here, our

**[00:24:12]** back-end dev did the work, communicated

**[00:24:14]** back to the lead, and here it's handing

**[00:24:16]** the results back to the orchestrator. We

**[00:24:18]** can see the results for our V1, our LR,

**[00:24:21]** and our new classifier here. All the

**[00:24:23]** results were written into the session.

**[00:24:24]** This session director is really

**[00:24:25]** important so that there's just a shared

**[00:24:27]** space for agents to operate on whatever

**[00:24:30]** work they're doing. We should be able to

**[00:24:31]** find head-to-head. There's the results

**[00:24:33]** and we can see the work that our

**[00:24:34]** multi-agent teams put together for us.

**[00:24:37]** You can see here we're running our

**[00:24:38]** original LR model against complement and

**[00:24:40]** B, and we have our accuracy across. The

**[00:24:43]** most important part about this

**[00:24:44]** classifier system, you know, jumping

**[00:24:45]** into the individual problem itself is

**[00:24:47]** that whenever we need a high

**[00:24:49]** intelligence model, we want our

**[00:24:50]** classifier to be more biased toward

**[00:24:52]** that. It's a much worse problem if you

**[00:24:54]** predicted a medium or low intelligence

**[00:24:57]** model when you really needed high,

**[00:24:58]** right? That's just a bad user

**[00:25:00]** experience, that's bad customer

**[00:25:01]** experience. So, we've fine-tuned the

**[00:25:03]** experience to make sure that things are

**[00:25:06]** pushed to high as a safe default. So,

**[00:25:09]** we're always pushing toward high, more

**[00:25:11]** expensive model for the customer

**[00:25:12]** experience. Based on the financials of

**[00:25:14]** your business, you might change that a

**[00:25:16]** little bit to veer toward mid, hopefully

**[00:25:18]** not low. That's kind of the details of

**[00:25:19]** how I would build out a prompt writing

**[00:25:21]** system and how I have built out some

**[00:25:23]** prompt writing systems in the past. As

**[00:25:25]** you've seen here, there are many things,

**[00:25:27]** there are many dimensions you can

**[00:25:28]** specialize on. Not only are we

**[00:25:30]** specializing in individual agents,

**[00:25:31]** anyone can do this with Cloud Code via

**[00:25:33]** sub-agents. We've actually built

**[00:25:35]** specialized teams. Every team has its

**[00:25:37]** domain, and then we're having a single

**[00:25:39]** interface orchestrator so that our

**[00:25:41]** cognitive input into the system, right?

**[00:25:43]** Your effort, it doesn't need to increase

**[00:25:46]** as you increase the total number of

**[00:25:48]** specialized agents. This is a huge

**[00:25:49]** problem with customization unless you

**[00:25:51]** build it right. And I think this

**[00:25:52]** chat-like interface is the right way to

**[00:25:55]** build it. Because here we have

**[00:25:56]** delegation pattern where it all starts

**[00:25:58]** with the orchestrator, right? You are

**[00:26:00]** just talking to the orchestrator, and

**[00:26:01]** then the orchestrator delegates to the

**[00:26:03]** teams, and the teams delegate to their

**[00:26:04]** workers. By doing this, every team

**[00:26:07]** focuses on their specialty, and every

**[00:26:09]** team is fine-tunable. Of course, you can

**[00:26:11]** see here I have all of my leads as a

**[00:26:14]** more powerful Opus model, and the

**[00:26:17]** workers are Sonic models. You could play

**[00:26:19]** with this, you could tune this however

**[00:26:20]** you like, but you can see the pattern

**[00:26:21]** very clearly, right? You want your

**[00:26:22]** thinkers, your orchestrator level, and

**[00:26:24]** your lead agents to be as smart as they

**[00:26:27]** possibly can. And then your workers, you

**[00:26:29]** can dial down, they just need to follow

**[00:26:30]** instructions and execute. Of course, if

**[00:26:32]** you're going all out, you'll make

**[00:26:33]** everything the top best possible model.

**[00:26:36]** I think a really important piece of this

**[00:26:37]** is the 1 million context window model. I

**[00:26:39]** back in Devs doing a lot of work, did

**[00:26:40]** get past 100K tokens spent, and this

**[00:26:43]** will just continue as knowledge and

**[00:26:45]** domain expertise stacks up in the code

**[00:26:47]** base. Nice part here is, you know,

**[00:26:49]** whenever you want to, you can just prune

**[00:26:52]** a team or a member or you can add a

**[00:26:54]** team. Really is as simple as updating

**[00:26:56]** the configuration file. Let me just

**[00:26:58]** quickly showcase that. We can just very

**[00:27:00]** quickly kill this team, hop back into

**[00:27:02]** the terminal, fire up the app, teams,

**[00:27:04]** and now it's just planning and

**[00:27:05]** engineering. No validation. Super

**[00:27:07]** powerful trend here. On the channel, I

**[00:27:09]** really like to focus on the idea of

**[00:27:11]** moving where the ball is going, not

**[00:27:13]** where it is. We have a lot of very

**[00:27:15]** powerful tailwinds available, but

**[00:27:17]** they're not accessible if you're doing

**[00:27:19]** what everyone else is doing. Let me

**[00:27:21]** share a few next generation ideas and

**[00:27:23]** ways that I will be and already am

**[00:27:25]** pushing multi-agent teams like this.

**[00:27:28]** Once you build an opinionated structure

**[00:27:30]** like this, the next thing to do is build

**[00:27:31]** a meta agent or meta team that helps you

**[00:27:34]** quickly fine-tune and improve the team.

**[00:27:37]** With the system, you can build out

**[00:27:39]** powerful things like team-based custom

**[00:27:41]** slash commands, aka skills. It's also

**[00:27:43]** called skills. There's so many names for

**[00:27:45]** just prompts. It's annoying. You can

**[00:27:46]** build out these prompts, these workflows

**[00:27:48]** with your teams in mind. You know, a

**[00:27:51]** classic one is like plan, build,

**[00:27:53]** validate. Like one of the oldest

**[00:27:55]** workflows known to agentic engineers.

**[00:27:56]** You have a plan, you build, and you

**[00:27:58]** validate just like how we wrote except

**[00:27:59]** as a reusable prompt. You can start

**[00:28:01]** really, really stacking this up and

**[00:28:02]** getting massive advantages with a system

**[00:28:04]** like this. Another idea here is a lot of

**[00:28:06]** the value of this system comes from your

**[00:28:09]** agents stacking up knowledge over time.

**[00:28:11]** So, our engineering lead, for instance,

**[00:28:13]** has its own mental model. And so, really

**[00:28:16]** fine-tuning the mental model and the

**[00:28:18]** mental model skill to properly track

**[00:28:21]** results in your system is going to be

**[00:28:22]** really important. You may have noticed

**[00:28:24]** here expertise is a list. So, we can

**[00:28:27]** also do something like this. If you have

**[00:28:29]** highly opinionated knowledge, you need

**[00:28:31]** to add to your database migration agent

**[00:28:34]** or your billing agent. It's a really,

**[00:28:36]** really important thing to have

**[00:28:37]** specialized or specific context. You

**[00:28:39]** don't want anyone to mess it up. So, you

**[00:28:41]** can build out additional expertise

**[00:28:43]** that's not updatable. Talking about that

**[00:28:45]** billing use case, billing workflow, blah

**[00:28:48]** blah blah. All of this context is

**[00:28:49]** specializable. This would create a

**[00:28:51]** read-only memory file of expertise that

**[00:28:55]** only your billing agent would have. This

**[00:28:57]** is one example, but again, expertise

**[00:29:00]** super super important. Billing,

**[00:29:01]** migrations, DevOps, deploying, these are

**[00:29:03]** all great examples of specialized

**[00:29:06]** engineering. You don't want a generic

**[00:29:08]** agent doing this stuff. You want an

**[00:29:09]** agent that has experience, that has

**[00:29:11]** expertise doing this over and over and

**[00:29:13]** over, just like you would trust someone,

**[00:29:15]** an engineer on your team who you know

**[00:29:17]** has done it, right? It's the same

**[00:29:19]** concept. Really locking in the expertise

**[00:29:21]** is going to be a massive advantage for

**[00:29:23]** engineers that are able to unlock it,

**[00:29:25]** and for engineers that understand why

**[00:29:27]** agent experts will always outperform a

**[00:29:30]** generic agent. Skills, very very clear

**[00:29:33]** why this is important. It's not a secret

**[00:29:35]** to anyone. Specialized tools, obviously

**[00:29:37]** very important. You can see how much

**[00:29:39]** power we built into the system with just

**[00:29:41]** one tool, delegate. And then of course,

**[00:29:43]** domain locking. You might have a

**[00:29:45]** configuration file agent or again,

**[00:29:47]** probably better example, DevOps agent.

**[00:29:49]** No one should be touching the DevOps

**[00:29:51]** files and folders except the DevOps

**[00:29:53]** agent. This is like the holy grail of

**[00:29:56]** operating mid to large-size codebases

**[00:29:58]** with these powerful agents that are

**[00:30:00]** continuing to get smarter, more

**[00:30:02]** intelligent while the token cost is

**[00:30:04]** coming down. I know a lot of engineers

**[00:30:06]** are going to watch this, and it always

**[00:30:08]** annoys me frankly. They're going to

**[00:30:09]** watch this and and they're going to see,

**[00:30:11]** "Oh my god, $8 for this agent team?

**[00:30:14]** You're wasting time and tokens

**[00:30:15]** communicating between these agents."

**[00:30:17]** You're thinking about right now. You're

**[00:30:19]** not thinking far enough into the future.

**[00:30:21]** Models will improve, costs are going

**[00:30:23]** down, tokens are going to be available

**[00:30:26]** to you at insane volumes. I think about

**[00:30:29]** this all the time. I am not spending

**[00:30:31]** enough tokens, you are not spending

**[00:30:32]** enough tokens, and you are wasting time

**[00:30:34]** doing things the old way, and now the

**[00:30:36]** old way is

**[00:30:38]** one agent to coding tool in the terminal

**[00:30:40]** prompting back and forth. I really,

**[00:30:42]** really highly recommend you push

**[00:30:43]** yourself to spend more tokens to do more

**[00:30:46]** work with agents. This is the greatest

**[00:30:48]** opportunity that has ever existed for us

**[00:30:51]** engineers. And now the only question is,

**[00:30:53]** can you agentic code? Can you agentic

**[00:30:57]** engineer? Can you build systems that

**[00:30:59]** build systems on your behalf? This is

**[00:31:02]** yet another powerful agentic opportunity

**[00:31:05]** available to you if you want to tap into

**[00:31:07]** it. This is not a public code base. I'm

**[00:31:10]** sharing this exclusively with Tactical

**[00:31:12]** Agentic Coding and Agentic Horizon

**[00:31:14]** members. This is the second of three

**[00:31:17]** next generation multi-agent applications

**[00:31:19]** and code bases I'll be sharing with

**[00:31:21]** Agentic Horizon members. So, let me just

**[00:31:23]** quick break this down as I did last

**[00:31:25]** week. Tactical Agentic Coding is my take

**[00:31:27]** on how to scale far beyond AI coding and

**[00:31:29]** vibe coding with agentic engineering. So

**[00:31:32]** powerful, your code base runs itself. I

**[00:31:34]** don't receive any sponsorships. I've

**[00:31:36]** been given plenty of opportunity to do

**[00:31:38]** so. All I sell on this channel is

**[00:31:40]** hand-crafted courses I built, which

**[00:31:43]** frankly these take years to build to

**[00:31:45]** like have the knowledge and the

**[00:31:46]** presentation abilities to even

**[00:31:47]** communicate these ideas. I take them all

**[00:31:49]** and I give them to you in these

**[00:31:51]** individual courses. So, that's all I

**[00:31:53]** sell on this channel. If you want to

**[00:31:54]** support, if you like the ideas, take

**[00:31:56]** this course and get ahead of the pack. A

**[00:31:58]** lot of what you're seeing in the

**[00:31:59]** industry we have covered already in this

**[00:32:01]** course. And there's information and

**[00:32:03]** patterns in this course that has not

**[00:32:05]** been covered in the industry at all yet.

**[00:32:07]** This is for engineers that ship. AI

**[00:32:09]** coding is not enough. You want to be

**[00:32:10]** building systems that build systems for

**[00:32:13]** you. This is the true gift of agentic

**[00:32:16]** coding, all right? You can compound your

**[00:32:18]** advantage by building agentic systems

**[00:32:20]** that then build your application, test

**[00:32:22]** your application, validate your

**[00:32:23]** application, plan on your application,

**[00:32:25]** so on and so forth, right? If you're

**[00:32:26]** using agents on a daily basis, this

**[00:32:28]** course was made for you. We talk about

**[00:32:30]** templating your engineering and scaling

**[00:32:32]** the core forward to their absolute

**[00:32:34]** maximum. Let me be super clear about

**[00:32:35]** this. There are two courses in this. If

**[00:32:37]** you want to gain access to the

**[00:32:38]** multi-team H entity coding tool and last

**[00:32:41]** week's CEO agents multi-agent code base

**[00:32:45]** where we use many agents and lots of

**[00:32:46]** compute to help us make strategic

**[00:32:48]** decisions. These are available for

**[00:32:50]** agentic Horizon members. So, you need

**[00:32:52]** both courses to gain access, but I

**[00:32:54]** guarantee you it's going to be worth it.

**[00:32:55]** There's a lot of valuable powerful ideas

**[00:32:57]** we talk about. We go through eight

**[00:32:58]** tactics of agentic coding. We build a

**[00:33:00]** system that builds a system. No AGI, no

**[00:33:03]** ASI BS. It's just boots on the ground

**[00:33:05]** engineering with agents. All right.

**[00:33:06]** Inside of agentic Horizon, we push all

**[00:33:08]** the ideas further. The most important

**[00:33:10]** one is building agentic layers. And as

**[00:33:13]** mentioned today, agent experts. For

**[00:33:15]** anyone who's hesitant or not sure or

**[00:33:17]** maybe this is the first time you're

**[00:33:18]** watching one of my videos, I only want

**[00:33:21]** you in this course if it's for you. For

**[00:33:23]** that reason, I have a no questions asked

**[00:33:25]** 30-day refund before you start lesson

**[00:33:27]** four. So, hop in here. Get your edge.

**[00:33:30]** I'm going to have these code bases

**[00:33:31]** available for agentic Horizon members.

**[00:33:34]** Phase three is coming soon. So, make

**[00:33:36]** sure you understand everything that's

**[00:33:38]** available to you right now in phase two

**[00:33:40]** in the age of agents. Many, many lessons

**[00:33:43]** in here breaking down lots of ideas

**[00:33:45]** you've already seen in the industry.

**[00:33:47]** That's enough for now on this. Again,

**[00:33:49]** link will be in the description for you

**[00:33:51]** if you're interested. The name of the

**[00:33:53]** game in 2026 is trust and scale. What

**[00:33:57]** can you do with your agentic coding

**[00:33:58]** tools and your agentic systems to

**[00:34:00]** increase the trust you have in your

**[00:34:03]** agents to such a high level that you

**[00:34:04]** know they will ship the result when you

**[00:34:06]** hit enter on the prompt. After you do

**[00:34:09]** that, you scale it. How big can you go?

**[00:34:12]** How surgical can your agents be? Agents

**[00:34:14]** with specialized expertise that builds

**[00:34:17]** over time will play a critical role

**[00:34:19]** here. This isn't just Claude capturing

**[00:34:21]** memory with everything you've ever said

**[00:34:23]** to it over years. That's not going to go

**[00:34:25]** well. What is going to go well is

**[00:34:27]** specialized agents that have specific

**[00:34:29]** purposes and growing context windows and

**[00:34:32]** increasing intelligence that you have

**[00:34:34]** learned to specialize in your agent

**[00:34:35]** harness. More tools like this will

**[00:34:37]** emerge, but the ideas will be there. And

**[00:34:40]** then the question becomes, do you know

**[00:34:42]** how to build agent experts? And then,

**[00:34:45]** can you build teams of experts that

**[00:34:47]** operate autonomously on your behalf? No

**[00:34:51]** matter what, stay focused and keep

**[00:34:53]** building.
