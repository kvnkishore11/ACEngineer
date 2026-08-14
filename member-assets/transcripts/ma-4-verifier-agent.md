# The Pi Verifier Agent

**Key:** `ma-4-verifier-agent`

**Source:** YouTube (see meta)

---

**[00:00:00]** What's up, engineers? Andy Dev Dan here.

**[00:00:02]** Today, I've got an absolute banger, a

**[00:00:04]** agentic system to share with you. But

**[00:00:06]** first, let's set the stage. April 2026

**[00:00:10]** at the highest velocity of model

**[00:00:12]** releases ever. We got Opus 4.7, GPT 5.5,

**[00:00:16]** DeepSeek V4, GLM 5.1, Kimmy Cat 2.6, and

**[00:00:21]** the Quinn series. The pace has been

**[00:00:23]** incredible, but for us engineers, model

**[00:00:26]** performance is no longer the bottleneck.

**[00:00:29]** It's you and I. It's our ability to

**[00:00:32]** extract value out of agentic systems at

**[00:00:36]** scale safely. If you look closely at any

**[00:00:38]** one of these benchmarks, you'll see

**[00:00:40]** something that's missing. Have you

**[00:00:42]** noticed it? It's hiding in plain sight,

**[00:00:44]** and once you realize it, every benchmark

**[00:00:47]** looks incomplete. So, instead of

**[00:00:49]** rehashing yet another model release,

**[00:00:51]** which we know will keep coming over

**[00:00:53]** time, let's talk about what we can do

**[00:00:55]** with combinations of models with every

**[00:00:58]** release moving forward. Here, I have two

**[00:01:02]** specialized pie coding agents, each

**[00:01:06]** running state-of-the-art cracked models.

**[00:01:08]** We have Opus 4.7 on the right, and we

**[00:01:11]** have GPT 5.5 on the left. I've

**[00:01:14]** customized these agent harnesses to

**[00:01:16]** deliver unique value, but you'll notice

**[00:01:18]** something weird here. This harness takes

**[00:01:21]** no input. What is this? How does it

**[00:01:24]** work? And what's missing from every

**[00:01:26]** benchmark? Let's break it down with the

**[00:01:28]** verifier agent.

**[00:01:35]** One of the highest leverage things you

**[00:01:37]** and I can do is increase the information

**[00:01:40]** density per action for agents in our

**[00:01:43]** production code bases. OpenAI's new GPT

**[00:01:46]** image 2 model is exceptional at this.

**[00:01:49]** So, let's use this new image generation

**[00:01:51]** model to showcase how the verifier

**[00:01:53]** works. In our builder agent on the right

**[00:01:55]** here, I'm going to prompt run prime,

**[00:01:57]** then run skill GBT image two, generate

**[00:02:00]** arch.jpg to concisely describe the

**[00:02:04]** architecture of the verifier two agent

**[00:02:07]** system. The prime command gets our agent

**[00:02:09]** essential context about this code base.

**[00:02:12]** You can see this customize pi agent

**[00:02:13]** going through the process. It's going to

**[00:02:15]** study the code base, understand how this

**[00:02:16]** works, and you can see here it's reading

**[00:02:18]** this GBT image two skill I've created to

**[00:02:21]** teach the agent how to generate and edit

**[00:02:23]** images with this new model. It's kicking

**[00:02:25]** off that script with a highly, highly

**[00:02:27]** detailed image prompt. This is one of

**[00:02:29]** the great parts about Claude Opus 4.7.

**[00:02:32]** It understands agents. It understands

**[00:02:34]** models. It knows that it itself can

**[00:02:37]** prompt other models. And you can push

**[00:02:39]** this ability by templating and teaching

**[00:02:41]** exactly how you want your prompts to be

**[00:02:43]** written. This is super, super key for

**[00:02:45]** prompting other models and agents, which

**[00:02:47]** is key for scaling our work beyond a

**[00:02:50]** single agent, which you'll see here. So,

**[00:02:52]** this will take some time. You can see

**[00:02:53]** here 70 seconds already. But the image

**[00:02:55]** quality coming out of the new GBT image

**[00:02:57]** 2.0 model is insane. It's worth the

**[00:03:00]** wait, and it's worth the price. Image

**[00:03:02]** generation is complete. The agent's

**[00:03:03]** checking its work. Now it's marking it

**[00:03:05]** done. Now watch what happens here once

**[00:03:07]** our builder agent completes.

**[00:03:10]** Excellent. And now our verifier agent

**[00:03:12]** has kicked off unprompted. We did not

**[00:03:15]** prompt this. I'm not doing anything

**[00:03:16]** here. My hands are off the keyboard. The

**[00:03:17]** verifier agent is now taking over. We

**[00:03:20]** have this very simple two agent system

**[00:03:23]** where on completion of any prompt that

**[00:03:25]** executes, the verifier is kicking off

**[00:03:28]** and doing work. Now the big question is,

**[00:03:31]** what is this agent doing? What is the

**[00:03:32]** work that's being accomplished here? You

**[00:03:34]** can see that it's reading the image that

**[00:03:36]** was generated. And now what's going to

**[00:03:37]** happen is it's going to validate a few

**[00:03:40]** things. The first thing it's going to do

**[00:03:41]** is validate the individual claims the

**[00:03:44]** builder agent has made. And then second,

**[00:03:46]** it's going to make sure that what we

**[00:03:48]** asked for is what it built. So, if we

**[00:03:50]** just hit up here on the builder agent,

**[00:03:52]** you can see exactly what we asked for.

**[00:03:54]** What's going to happen here is our

**[00:03:55]** verifier is going to walk through every

**[00:03:57]** single claim. There we go, check this

**[00:03:59]** out. And if it needs to, it's going to

**[00:04:01]** prompt the primary agent. So, this is

**[00:04:03]** really incredible. I didn't prompt this.

**[00:04:05]** My verifier agent just prompted my

**[00:04:08]** builder agent. Let's make this super

**[00:04:09]** clear. This prompt here from the

**[00:04:11]** verifier kicked off a prompt in our

**[00:04:13]** builder agent. The verifier agent found

**[00:04:16]** something that was incorrect. Let's go

**[00:04:18]** ahead and see if it's written up its

**[00:04:19]** report here. Okay, it has. Fantastic.

**[00:04:21]** So, let's go ahead and let that image

**[00:04:22]** generate, and let's break down the

**[00:04:23]** feedback here. You can see that our

**[00:04:25]** input here is prompted builder. This is

**[00:04:28]** feedback mode. Our verify agent here has

**[00:04:30]** given our primary agent feedback.

**[00:04:33]** Completely unprompted. Again, I did

**[00:04:35]** nothing here. This system is acting on

**[00:04:37]** its own. So, what happened here, right?

**[00:04:39]** On every prompt on the stop hook, the

**[00:04:41]** builder agent sends an event through a

**[00:04:43]** Unix socket. Actually, we should take a

**[00:04:44]** look at this image before it gets

**[00:04:46]** updated. So, we're going to open up VS

**[00:04:47]** Code, and let's look at this

**[00:04:48]** architecture diagram. Here, a very

**[00:04:50]** detailed image generated by GBT image

**[00:04:53]** 2.0. The text styling and pretty much

**[00:04:56]** everything coming out of this model is

**[00:04:58]** very, very state-of-the-art. You can ask

**[00:05:00]** for exactly what you want to see, and

**[00:05:01]** it'll generate it for you. But, you can

**[00:05:03]** see a solid description and solid

**[00:05:05]** understanding. And in fact, before this

**[00:05:07]** gets overwritten, I'm just going to

**[00:05:08]** clone it here so we have it as a backup.

**[00:05:10]** What's happening in this report? Status

**[00:05:12]** failed. Our agent's work was not

**[00:05:13]** successful. Status failed. Confidence is

**[00:05:16]** feedback. What did you verify? GBT image

**[00:05:18]** 2 was used. It ran the red script from

**[00:05:20]** the red skill. The image was generated.

**[00:05:22]** It validated that it existed. Right file

**[00:05:24]** size. It is a JPG image as asked.

**[00:05:27]** Validated the claims. Everything the

**[00:05:29]** builder said that it did. And then the

**[00:05:31]** model is looking visually at the image

**[00:05:34]** to make sure that it describes the

**[00:05:35]** verifier two-agent system, which is the

**[00:05:37]** code base that we're generating the

**[00:05:39]** architecture diagram for. Readability

**[00:05:41]** and text density looks good. It could

**[00:05:43]** verify everything it needed to, very

**[00:05:44]** important. But, check this out. Our

**[00:05:46]** agent gave feedback. And you can see

**[00:05:48]** here the work is completed. Our builder

**[00:05:50]** agent violated one of the rules, okay?

**[00:05:53]** And so we were just getting to that. Let

**[00:05:54]** me just pause this, scroll back up. You

**[00:05:56]** can see that next stop hook is coming

**[00:05:57]** over. What feedback did you give?

**[00:05:59]** ArchJBG existed visually, shows the

**[00:06:01]** verifier to agent system, but violates

**[00:06:03]** the readability contract by exceeding 10

**[00:06:06]** distinct blocks. Inside of the verifier

**[00:06:08]** agent for image generation, we have a

**[00:06:10]** rule that we should never have more than

**[00:06:12]** 10 blocks of text inside any image. So

**[00:06:16]** this is just a great rule for building

**[00:06:18]** out diagrams. This looks good, but it is

**[00:06:20]** overloaded with information. There's a

**[00:06:22]** lot going on. It takes time to digest

**[00:06:24]** this, right? An image should be worth a

**[00:06:25]** thousand words. It shouldn't force you

**[00:06:27]** to work through things and read a ton of

**[00:06:29]** text. That's what text is for. It really

**[00:06:31]** simplified that for us. And so this is

**[00:06:33]** one of the rules we have that we

**[00:06:35]** directly built into our verifier. And so

**[00:06:37]** that was feedback that our verifier

**[00:06:39]** directly gave our verifiable agent or

**[00:06:43]** just the builder agent. So if we scroll

**[00:06:44]** down here, we can see that that second

**[00:06:46]** prompt was completed and now it has an

**[00:06:48]** updated status, right? Now we have a

**[00:06:50]** clean green bar here. We have a

**[00:06:52]** successful bar. Verify image, verified,

**[00:06:55]** perfect. In the bottom section here in

**[00:06:57]** this report format, we're being very

**[00:06:58]** consistent. Turn index one, we have our

**[00:07:00]** total atomic claims, and then we have

**[00:07:03]** our claims verified, claims failed,

**[00:07:05]** claims unverified. And we got seven out

**[00:07:08]** of seven verified. So everything was

**[00:07:09]** successful. Our verifier agent did not

**[00:07:12]** reprompt our primary agent. I hope you

**[00:07:14]** kind of see the value proposition of

**[00:07:17]** having an agent that just observes, that

**[00:07:19]** just watches, and only gives feedback

**[00:07:22]** when necessary. And speaking of

**[00:07:23]** feedback, we have a couple really

**[00:07:25]** important key sections here that is

**[00:07:27]** going to help us improve this system.

**[00:07:29]** What could you not verify? As you can

**[00:07:31]** imagine, this will be very important for

**[00:07:34]** us improving our verifier agent. This

**[00:07:36]** verifier agent has a lot of special

**[00:07:38]** properties built into it. So let's go

**[00:07:40]** ahead out that image that was generated.

**[00:07:42]** You can see here, this second version

**[00:07:43]** much better, right? A lot less text

**[00:07:46]** overloaded. This is an image, not a

**[00:07:48]** markdown file. So, we want it to be

**[00:07:50]** super clear, super concise, and this is

**[00:07:53]** the Pi Verifier agent architecture

**[00:07:54]** builder agent, and we have a verifier.

**[00:07:56]** They communicate through a local Unix

**[00:07:58]** socket. It has a few guardrails and

**[00:08:01]** constraints that we're going to talk

**[00:08:02]** about in a moment here, and the verifier

**[00:08:04]** takes in the session file. Thanks to the

**[00:08:06]** Pi agent harness, we have full access to

**[00:08:08]** everything our builder agent has done.

**[00:08:11]** And our verifier can just look at that

**[00:08:13]** at any point in time, and if it needs

**[00:08:14]** to, only if it's violated a rule of the

**[00:08:17]** verifier, does it actually re-prompt.

**[00:08:19]** This system looks good. I want to add

**[00:08:21]** something to this image. Let's go ahead

**[00:08:22]** and push this new GPT image to model a

**[00:08:24]** little bit. It's missing one thing. It's

**[00:08:26]** missing us in this picture. I'll say

**[00:08:28]** this, are the ones prompting the

**[00:08:30]** verifiable, also known as the builder.

**[00:08:34]** So, we'll fire that off, and another

**[00:08:36]** round is going to occur. This is one of

**[00:08:38]** the keys of this system. I am just

**[00:08:40]** working on a single agent harness, a

**[00:08:43]** single agent encoding tool, as you do.

**[00:08:45]** Check out the compute I'm spending here

**[00:08:46]** on the left to verify all the claims and

**[00:08:49]** to write the prompts that I would have

**[00:08:51]** had to write myself anyway. Here we go.

**[00:08:53]** Opus getting to work, doing the

**[00:08:55]** building, and after it builds, GPT 5.5

**[00:08:57]** is going to get its back. It's going to

**[00:08:59]** check its work. It's going to make sure

**[00:09:01]** that it's doing the right thing. We are

**[00:09:02]** pair programming. Let's be super clear

**[00:09:04]** about this. We have two agents working

**[00:09:06]** together in a very, very simplified

**[00:09:09]** multi-agent system. On the channel,

**[00:09:10]** we've talked about teams of agents.

**[00:09:12]** We've broken down a three-layer

**[00:09:14]** architecture where you have an

**[00:09:15]** orchestrator, leads, and worker agents.

**[00:09:17]** Very powerful, very complex. Here, we're

**[00:09:20]** simplifying. We're focusing on one of

**[00:09:22]** the first, most important multi-agent

**[00:09:24]** systems that you can probably build. And

**[00:09:26]** I have to tell you, you know, many of

**[00:09:27]** the ideas I share with you here are

**[00:09:29]** experiments. Many of the ideas are trial

**[00:09:31]** and error. This is one of the systems

**[00:09:32]** that, as soon as I found this, I put

**[00:09:34]** this in my pocket.

**[00:09:36]** And this is a system I'm using a lot

**[00:09:39]** right now. And this is a good time to

**[00:09:40]** start talking about the benefits of this

**[00:09:41]** system. What problem does the verifier

**[00:09:44]** agent solve for you? What does this

**[00:09:45]** unlock for you? Let's talk about this.

**[00:09:52]** Whenever you can, you should be spending

**[00:09:54]** tokens to save time. As you saw here

**[00:09:56]** with my image generation system, people

**[00:09:59]** don't like noisy images with a bunch of

**[00:10:01]** text that you have to reason through.

**[00:10:03]** So, I built it into my image

**[00:10:04]** verification agent that for every image

**[00:10:06]** you see, it cannot be bloated with text.

**[00:10:10]** 10 blocks of text is the limit. And so,

**[00:10:12]** this is a very, very powerful system.

**[00:10:13]** I'm spending more tokens, and you can

**[00:10:15]** see here 4% on Opus, 23% on GPT 5.5.

**[00:10:19]** Quite literally spending 5x tokens to

**[00:10:22]** make sure that I spend less of my time.

**[00:10:25]** And this is an interesting equation you

**[00:10:26]** can do. How much is your time worth? If

**[00:10:29]** you ask me, your time is worth a

**[00:10:31]** ton. You should not be trading your time

**[00:10:34]** for anything you don't have to, or for

**[00:10:36]** anything that you don't want to. And so,

**[00:10:38]** one of the key value propositions of the

**[00:10:40]** system is that we are scaling our

**[00:10:42]** compute to scale our impact. We are

**[00:10:43]** directly spending more tokens to save

**[00:10:46]** time. What are we spending more tokens

**[00:10:48]** and saving time on? That's the next big

**[00:10:51]** value proposition. And let me go ahead

**[00:10:52]** and write these out, right? Let's be

**[00:10:53]** super explicit about the value that

**[00:10:55]** we're actually getting out of this

**[00:10:56]** system. So, what's the value of the

**[00:10:57]** verifier agent? Spend tokens to save

**[00:10:59]** time. And so, what are we saving time

**[00:11:01]** doing? Review constraint. Time is worth

**[00:11:04]** more. So, what are we actually spending

**[00:11:06]** our tokens on? We're spending our tokens

**[00:11:07]** on breaking through the review

**[00:11:09]** constraint of AGC, agent decoding.

**[00:11:12]** Right, let me just spell this out. In

**[00:11:13]** agent decoding, there are two

**[00:11:15]** constraints. If you're agent and

**[00:11:16]** engineering properly, you have already

**[00:11:18]** noticed this. Planning and reviewing. If

**[00:11:20]** you're doing things right, you're

**[00:11:21]** spending your time planning and

**[00:11:22]** reviewing. With the verifier agent, we

**[00:11:25]** can improve our review constraint. How?

**[00:11:27]** By teaching an agent exactly how we

**[00:11:30]** verify. By adding these rules, by making

**[00:11:32]** them read the files that you would read.

**[00:11:34]** This is a very, very clear, concise

**[00:11:36]** example for you. When this agent runs,

**[00:11:38]** and I'm generating images, I'm always

**[00:11:41]** going to run a validator behind it to

**[00:11:43]** make sure that it didn't violate any of

**[00:11:44]** the rules for image generation that I

**[00:11:47]** have set. And this allows me to do

**[00:11:49]** something really special. We'll talk

**[00:11:50]** about this at the end, but I can just

**[00:11:51]** continue to stack up these verifier

**[00:11:54]** agents to focus on one specific thing.

**[00:11:56]** We're hitting on this key tactic of

**[00:11:58]** agenda coding once again. One agent, one

**[00:12:00]** prompt, one purpose. A focused agent is

**[00:12:03]** a performant agent. These validators,

**[00:12:05]** these verifiers, just focus on one

**[00:12:08]** thing. They make sure that that one

**[00:12:09]** thing is right. You can see here, you

**[00:12:11]** know, we're working through image

**[00:12:13]** generation as a concise example, but now

**[00:12:15]** every image I generate is going to run

**[00:12:17]** through a check, a series of constraints

**[00:12:20]** that are validated

**[00:12:22]** non-deterministically, and as you'll see

**[00:12:23]** in our upcoming example,

**[00:12:25]** deterministically as well. And so this

**[00:12:27]** is another advantage of this system.

**[00:12:29]** We're spending tokens to save time. And

**[00:12:32]** what do these tokens do? They help us

**[00:12:33]** break through the review constraint.

**[00:12:34]** We're teaching our agents how to review

**[00:12:37]** and verify the work. And you can see

**[00:12:38]** everything that our agent verified by

**[00:12:41]** hand. We have nine sets of text blocks

**[00:12:43]** here, and it spelled them all out

**[00:12:45]** individually, which is fantastic. You

**[00:12:47]** know, GPT 5.5 is one of the best image

**[00:12:50]** reading models. There was no feedback to

**[00:12:52]** give, so it just stopped, right? And it

**[00:12:54]** wrote this report for us. It didn't give

**[00:12:55]** any feedback, and it doesn't need

**[00:12:57]** anything from us to verify this next

**[00:12:59]** time. This leads us into the next huge,

**[00:13:01]** huge, huge value proposition of this

**[00:13:03]** verifier agent specifically. You'll

**[00:13:05]** notice here, we have a feedback loop.

**[00:13:08]** This field here, this report section

**[00:13:10]** that this agent always reports in,

**[00:13:12]** because I prompt engineered the system

**[00:13:15]** prompt. If there's ever something the

**[00:13:16]** agent can't actually verify, it will

**[00:13:19]** tell me. It will say it right here. And

**[00:13:21]** guess what I can do with this? This is a

**[00:13:22]** positive feedback loop. It's a flywheel.

**[00:13:25]** I can then, if I need to, take the

**[00:13:27]** information given me here on what it

**[00:13:28]** could not verify, and I can encode this,

**[00:13:31]** I can template this into the agent's

**[00:13:33]** system prompt. And let's go ahead and

**[00:13:35]** just take a look at this one. We have an

**[00:13:36]** entire customized system prompt. This is

**[00:13:38]** not an average system prompt. I'm adding

**[00:13:40]** things into the front matter of this

**[00:13:42]** prompt to override and get special

**[00:13:44]** behavior. This is what you can do when

**[00:13:46]** you own the agent harness. More on that

**[00:13:48]** in a moment. But you can see here that I

**[00:13:49]** have a bunch of rules and verification

**[00:13:52]** steps that our verifier follows. And we

**[00:13:55]** can just search this, max text elements,

**[00:13:58]** right here, right? In our instructions,

**[00:13:59]** okay? So, it's super clear. If we look

**[00:14:01]** at the report, we are teaching our agent

**[00:14:04]** how to respond as well, where we have

**[00:14:06]** this clean, clear report section. What

**[00:14:08]** could you not verify, and what do you

**[00:14:10]** need from me to verify this next time?

**[00:14:13]** Super, super important. Why do we care

**[00:14:15]** about the verifier agent? It's because

**[00:14:17]** we have built-in positive feedback

**[00:14:19]** loops. I always advocate that you get

**[00:14:21]** out the loop, but it's important to be

**[00:14:23]** in the loop for certain work. And since

**[00:14:25]** you're there, you might as well be

**[00:14:27]** compounding the advantages of the agents

**[00:14:30]** you're working in and working on. This

**[00:14:32]** is one of the ways you can do this. Last

**[00:14:34]** but not least, template your engineering

**[00:14:36]** as a habit. Let's be super clear about

**[00:14:38]** this. The most important piece about

**[00:14:40]** this verifier agent is that we have

**[00:14:42]** templated our engineering into the

**[00:14:44]** system prompt of this agent, and then

**[00:14:46]** we've wrapped it inside of a custom Pi

**[00:14:49]** agent harness, where I actually cannot

**[00:14:51]** do anything but follow the rules of this

**[00:14:53]** system, right? I can't prompt this. I

**[00:14:56]** cannot fall to the lowest-hanging fruit

**[00:14:58]** of the generative AI age. There's no

**[00:14:59]** vibe coding this stuff. I cannot just

**[00:15:01]** fire a one-off prompt. I can't say, "Do

**[00:15:03]** XYZ." I cannot even interact with the

**[00:15:05]** verifier. That means that if something

**[00:15:07]** goes wrong here, if the verifier isn't

**[00:15:09]** verifying something, if it's missing

**[00:15:10]** something, if I need to add something to

**[00:15:12]** the system, there's no one-offs. I am

**[00:15:14]** forced to template my engineering into

**[00:15:17]** my verifier agent. This is very, very

**[00:15:19]** important. There's an increasing gap

**[00:15:21]** between the two key sets of engineers.

**[00:15:23]** Engineers who are stuck in the loop

**[00:15:26]** prompting back and forth with their

**[00:15:27]** agents. You're here. You're prompting

**[00:15:29]** back and forth. And then there's this

**[00:15:30]** second set. They're starting to build

**[00:15:32]** systems like the verifier agent. They're

**[00:15:34]** starting to build multi-agent systems

**[00:15:35]** that scale. They're building AI

**[00:15:37]** developer workflows, a key topic we talk

**[00:15:39]** about in tactical agentic coding.

**[00:15:41]** They're building something like Stripe's

**[00:15:43]** blueprint system, which we covered in a

**[00:15:45]** previous video. They are stacking up

**[00:15:47]** code plus agents to outperform either

**[00:15:50]** alone to run longer threads of work. If

**[00:15:53]** you're stuck prompting back and forth,

**[00:15:54]** you will not get those advantages. And

**[00:15:56]** here we are forcing ourselves to get

**[00:15:59]** that advantage. Okay, we're building it

**[00:16:00]** into the tool we're using. This is very

**[00:16:02]** important. These tools haven't emerged

**[00:16:04]** into the true form of what it means to

**[00:16:07]** be an agentic engineer. They don't fit

**[00:16:09]** the shape of what we are becoming yet,

**[00:16:11]** of the new role that we are adopting and

**[00:16:14]** and creating. But this is a step in that

**[00:16:16]** direction. I can't prompt this. I'm

**[00:16:19]** forcing myself to get out the loop. This

**[00:16:22]** is super super powerful. So this forces

**[00:16:24]** me to template my engineering. If

**[00:16:25]** something goes wrong, I don't just fire

**[00:16:27]** off another prompt. I'm effectively

**[00:16:29]** forced to improve one or more of the

**[00:16:31]** core four, context, model, prompt, or

**[00:16:33]** tools. So this is the other big

**[00:16:35]** advantage, as a habit by force. That's

**[00:16:38]** kind of the other thing, right? Um

**[00:16:40]** thanks to the agent harness. And I'll be

**[00:16:42]** super specific here. This is a

**[00:16:43]** customized agent harness, not just any

**[00:16:45]** agent harness. I have a dedicated

**[00:16:47]** workflow that is built in here. Now that

**[00:16:49]** you understand the benefits of a

**[00:16:51]** verifier agent, a simple two-agent

**[00:16:52]** system, let's go ahead and dive a little

**[00:16:54]** bit deeper here, right? Let me show

**[00:16:55]** another example and an additional key

**[00:16:57]** attribute of this system. And if we

**[00:16:59]** quickly check the architecture diagram

**[00:17:01]** created, you can see that this looks

**[00:17:03]** great, even better from our original

**[00:17:05]** version. We ran two prompts and we got a

**[00:17:07]** nice improved hero image. This looks

**[00:17:09]** great. I'm going to use this for this

**[00:17:11]** application as a hostess. And I'll be

**[00:17:13]** giving away two versions of the verifier

**[00:17:15]** agent, so stick around to the end to

**[00:17:17]** figure out which version will be

**[00:17:18]** available to you. As an engineer, you're

**[00:17:20]** never just reviewing one thing. You're

**[00:17:21]** reviewing sets of things, and that's the

**[00:17:23]** great part about this system. If we have

**[00:17:24]** J, we can see all the commands. This is

**[00:17:27]** a just It is a simple command-line

**[00:17:28]** runner. I use this in every single code

**[00:17:30]** base now, and we're going to boot up J

**[00:17:32]** the SQL. We're trying out one more key

**[00:17:34]** example here. And here we're using the

**[00:17:36]** JLM 5.1 model find all SQLite DBs in

**[00:17:39]** this repo breakdown tables, columns, and

**[00:17:43]** relationships.

**[00:17:44]** Now we have a verify SQLite agent, and

**[00:17:48]** one of the key things you may be notice

**[00:17:50]** here is that the verifier is independent

**[00:17:52]** of the verifiable. And this means that

**[00:17:55]** you can do whatever you want. You can

**[00:17:57]** run however many agents. You can set up

**[00:17:59]** whatever pi agent harness in this

**[00:18:01]** primary agent however you want to. What

**[00:18:03]** we're doing here is creating an

**[00:18:04]** extension that is layered on top of

**[00:18:07]** whatever your primary agent is that adds

**[00:18:09]** serious customized specialized

**[00:18:12]** validation. All the relationships, all

**[00:18:14]** the tables, all the SQLite databases in

**[00:18:17]** the system were found and were reported.

**[00:18:19]** The agent, right, this is Claude Opus

**[00:18:21]** 4.7. It's an absolutely cracked model.

**[00:18:23]** It did the work. But, there is no harm

**[00:18:25]** in having agent validate that that is

**[00:18:27]** true. And so, once again, the verifier

**[00:18:29]** agent is getting to work. We have a

**[00:18:30]** nice, powerful, yet cheap JLM 5.1 model

**[00:18:33]** here doing something really powerful.

**[00:18:35]** So, how this system works is is super

**[00:18:37]** important. You can see here the agent

**[00:18:39]** broke up the work into atomic claims.

**[00:18:42]** Everything you prompt into your agents,

**[00:18:44]** they're all small axioms. They're small

**[00:18:47]** claims. They're units of information

**[00:18:49]** that can be proven true or proven false.

**[00:18:52]** For instance, find all SQLite databases

**[00:18:54]** in this repo. So, this is something that

**[00:18:56]** is validatable. Did the builder agent

**[00:18:58]** actually find all the SQLite databases?

**[00:19:01]** Break down the tables. That is another

**[00:19:03]** thing that can be validated and proven.

**[00:19:05]** Did the agent break down the tables and

**[00:19:07]** the columns and the relationships? There

**[00:19:09]** are several claims and provable steps,

**[00:19:13]** right? Provable pieces of information

**[00:19:15]** that the verifier can work on. And this

**[00:19:17]** is part of the system prompt of this

**[00:19:19]** customized agent. It is a custom agent.

**[00:19:21]** It is built to break the prompts and the

**[00:19:23]** work done down into individual claims,

**[00:19:26]** right? Individual atomic claims,

**[00:19:29]** individual units of truth or false. And

**[00:19:31]** so you can see that here, right? What

**[00:19:32]** did you verify? Look at all these atomic

**[00:19:34]** claims. Look at all these individual

**[00:19:35]** things the agent has proven. Very, very

**[00:19:37]** powerful. Everything's true. This is a

**[00:19:39]** simple find and report. And if you

**[00:19:41]** scroll up here, you'll see that the

**[00:19:43]** agent is also doing something really

**[00:19:45]** interesting. I have restricted this

**[00:19:47]** agent. Once again, we have one agent,

**[00:19:48]** one prompt, and one purpose. This agent

**[00:19:51]** is restricted to running just this one

**[00:19:53]** script. We can see that inside of its

**[00:19:56]** system prompt here. So, inside of pi

**[00:19:58]** verifier agents, of course, when you're

**[00:20:00]** building your own customized pi agents,

**[00:20:02]** you can set up whatever directory

**[00:20:03]** structure you want. You're in full

**[00:20:04]** control when you control your agent

**[00:20:06]** harness. When you're not, you can't.

**[00:20:08]** We're doing something really special

**[00:20:09]** here. We're giving access to several

**[00:20:11]** sets of tools here, but also we have a

**[00:20:13]** bash policy. Not sure if you noticed,

**[00:20:15]** the number of security vulnerabilities

**[00:20:17]** is hitting the roof. It's going

**[00:20:19]** parabolic. And also, not sure if you

**[00:20:21]** noticed, but the number of times an

**[00:20:23]** agent is losing control, hallucinating,

**[00:20:26]** or just ignoring instructions is going

**[00:20:28]** up as well. If you're harness

**[00:20:30]** engineering properly and less

**[00:20:31]** controllable agent harnesses like cloud

**[00:20:33]** code, codex, Gemini, open code, yada

**[00:20:35]** yada yada. If you're using those, you

**[00:20:37]** can control what your bash tool can do.

**[00:20:40]** Let me make this super clear. The bash

**[00:20:41]** tool is the most dangerous tool you can

**[00:20:43]** give your agents. I'm going to talk

**[00:20:44]** about this more on the channel. Make

**[00:20:45]** sure you like, make sure you subscribe,

**[00:20:47]** but this tool is a ticking time bomb.

**[00:20:50]** And so what I've done here in my

**[00:20:51]** verifier agent is I've restricted it to

**[00:20:54]** using just one script. This is the

**[00:20:56]** highest level of control you can give.

**[00:20:59]** And so, if at any time this model calls

**[00:21:02]** anything with the bash tool other than

**[00:21:04]** my script, it's blocked, fully blocked.

**[00:21:06]** And so this is one of the things I've

**[00:21:07]** built into the system. SQLite agent,

**[00:21:09]** think about this, this can be your

**[00:21:11]** Postgres agent, this can be your

**[00:21:12]** whatever cloud DB agent, your MongoDB

**[00:21:15]** agent, MySQL agent, whatever back-end

**[00:21:18]** SQL blah blah blah you use, replace this

**[00:21:20]** with that, right? That's the idea here.

**[00:21:22]** And with this, it's very, very powerful,

**[00:21:24]** right? Especially for data manipulation

**[00:21:27]** related activities or agents are taking.

**[00:21:29]** Having a verifier is extraordinarily

**[00:21:31]** powerful because your agent might only

**[00:21:33]** find some of the data. It might only

**[00:21:35]** report some of the tables. With a

**[00:21:36]** verifier, it can come in and just

**[00:21:38]** double-check. And And once again, notice

**[00:21:40]** Opus spent 1% of its tokens, so it's

**[00:21:42]** something like, you know, 10K tokens.

**[00:21:44]** GLM 5.1, this is a 200K token context

**[00:21:46]** window model. So, what is that? 10%?

**[00:21:48]** That's 20K. So, this model spent two

**[00:21:51]** times the tokens verifying this agent

**[00:21:53]** than the actual agent execution. I'm

**[00:21:55]** spending 2x compute. Once again, I'm

**[00:21:56]** spending tokens to save time. And what

**[00:21:59]** I'm actually doing here is a little more

**[00:22:01]** important than you might see. I am

**[00:22:02]** increasing the trust I have in my agent

**[00:22:05]** system by having this verifier agent

**[00:22:07]** validate the atomic claims that the

**[00:22:10]** builder agent has performed. And so,

**[00:22:12]** once again, same prompt format, same

**[00:22:15]** verification set, same set of confidence

**[00:22:17]** levels it can report, nothing it could

**[00:22:18]** verify, no feedback, and no improvements

**[00:22:21]** for the verifier agent to improve for

**[00:22:23]** the next run. This is a compounding

**[00:22:25]** system. This is a system that's going to

**[00:22:27]** improve with every prompt I write. And

**[00:22:29]** hint hint, as I mentioned, you can stack

**[00:22:31]** more than one of these verifier agents.

**[00:22:33]** I'm not going to show that here. I don't

**[00:22:34]** have enough time. But, this is one of

**[00:22:35]** the patterns I've been using a lot and

**[00:22:38]** I'm getting a lot of value out of this.

**[00:22:40]** So, that's the core of this system. We

**[00:22:42]** have a two-agent multi-agent team. One

**[00:22:45]** is a verifier and one is whatever your

**[00:22:46]** normal agent is. And this could be

**[00:22:48]** running anything you want it to. This is

**[00:22:50]** just your primary PyCoding agent. On the

**[00:22:52]** left here, though, as mentioned in the

**[00:22:54]** beginning, we're validating all the

**[00:22:55]** claims that the builder agent made, and

**[00:22:58]** we're making sure that what we asked for

**[00:23:00]** is what was built. Okay, we're directly

**[00:23:02]** attacking the review constraint of a

**[00:23:05]** gentle coding. And this is where most

**[00:23:06]** engineers spend their time. Let me make

**[00:23:08]** this even clearer if I can here. Thanks

**[00:23:10]** to this two agent system, I'm spending

**[00:23:12]** less of my time reviewing work. This is

**[00:23:14]** the problem to solve. Multi-agent

**[00:23:16]** orchestration is the solution. So, let's

**[00:23:19]** come up, right? I'm not going to spend

**[00:23:20]** too much time on this code. You're going

**[00:23:21]** to have this available to you to kind of

**[00:23:23]** break down and understand and you'll be

**[00:23:24]** able to throw your agents at this with

**[00:23:26]** some really clear architecture diagrams.

**[00:23:27]** You know, in the beginning I said

**[00:23:29]** something's missing from all these

**[00:23:30]** benchmarks. What is it?

**[00:23:36]** As you can see here, every single model

**[00:23:37]** benchmark you look at, they're all

**[00:23:39]** making the exact same mistake from the

**[00:23:41]** perspective of us engineers. So, every

**[00:23:43]** one of these benchmarks is running a

**[00:23:44]** single model in isolation. Now, you

**[00:23:47]** might be thinking, "Yeah, obviously

**[00:23:49]** we're testing the individual models."

**[00:23:50]** But, my point here is that to get

**[00:23:52]** maximum intelligence out of these

**[00:23:54]** models, to get the true capabilities,

**[00:23:56]** you don't just run one of these models.

**[00:23:58]** You run multiple models. And most

**[00:24:01]** importantly,

**[00:24:02]** you know, we're not just kidding off sub

**[00:24:03]** agents. I'm not talking about

**[00:24:04]** delegation. I'm talking about

**[00:24:06]** multi-agent orchestration. I'm talking

**[00:24:08]** about setting up systems of agents. I'm

**[00:24:11]** talking about setting up teams of agents

**[00:24:13]** that operate better together than alone.

**[00:24:16]** We're not just talking about simple

**[00:24:16]** delegation. We're talking about

**[00:24:17]** coordinated agents. We are talking about

**[00:24:19]** multi-agent orchestration. We've been

**[00:24:21]** talking about this on the channel week

**[00:24:23]** after week after week, and I will be

**[00:24:25]** continuing to hammer on this idea

**[00:24:26]** because every benchmark is missing the

**[00:24:28]** true capability of what you can really

**[00:24:31]** do with these models. It's not about GPT

**[00:24:34]** 5.5 or Opus 4.7. It's GPT 5.5 and Opus

**[00:24:39]** 4.7, right? It's an and, not an or. Once

**[00:24:42]** again, you got to get out of this simple

**[00:24:44]** competitive mindset. Stack intelligence.

**[00:24:47]** Orchestrate intelligence. And a key part

**[00:24:50]** of this is owning your agent harness.

**[00:24:53]** This is why I've been such a fan of the

**[00:24:55]** pie coding agent. Looks like we got a

**[00:24:57]** website update. I'm not a huge fan of

**[00:24:59]** this italic font, kind of hard to read,

**[00:25:01]** but anyway,

**[00:25:03]** you know, the idea here is simple. There

**[00:25:04]** are many coding agents, there are many

**[00:25:06]** agent harnesses, but this one is yours.

**[00:25:08]** Fully customizable, adaptable, and it

**[00:25:11]** doesn't change underneath your feet as

**[00:25:13]** soon as a new update rolls out. You can

**[00:25:15]** control it, it's yours. This has been

**[00:25:17]** one of the most valuable and simplest

**[00:25:19]** one, so I wanted to come to the channel

**[00:25:20]** and share with you here. As mentioned,

**[00:25:22]** I'll be sharing two versions of the

**[00:25:24]** verifier agent. One is going to be

**[00:25:26]** available for free for you on my GitHub

**[00:25:28]** repository. I'm going to make this

**[00:25:30]** public for you, and the other one is

**[00:25:32]** going to be a souped-up version with a

**[00:25:34]** couple additional bells and whistles,

**[00:25:36]** and that's going to be available

**[00:25:37]** exclusively for tactical agentic coding

**[00:25:40]** and agentic horizon members. What is

**[00:25:42]** this? I'm going to quickly pitch this.

**[00:25:44]** If you've already seen this, you know,

**[00:25:45]** good time to sign off. This is my take

**[00:25:47]** on how to scale far beyond AI coding and

**[00:25:49]** vibe coding with advanced agentic

**[00:25:50]** engineering so powerful your code base

**[00:25:52]** runs itself. A lot of what you're seeing

**[00:25:54]** right now with multi-agent

**[00:25:56]** orchestration, we have covered, we have

**[00:25:57]** foreseen inside of this course. There

**[00:26:00]** are thousands of engineers inside this

**[00:26:02]** course, and let me be super clear here.

**[00:26:03]** This is for engineers that shipped

**[00:26:04]** production. If you're a vibe coder, if

**[00:26:06]** you're a new newbie engineer, this is

**[00:26:09]** not for you. This is not simple. This is

**[00:26:11]** not for beginners. I built this for the

**[00:26:12]** top 20% of actual software engineers,

**[00:26:15]** okay? But there are a couple things here

**[00:26:17]** that we cover. Let me just cover a

**[00:26:18]** couple facts. AI coding was just the

**[00:26:20]** beginning, phase one. Vibe coding is the

**[00:26:22]** lowest hanging fruit. 95% of all code

**[00:26:24]** bases are now outdated and inefficient.

**[00:26:26]** As we discussed, you, the engineer, are

**[00:26:28]** the bottleneck. It's not the models.

**[00:26:30]** It's not the tools. It's not the agents.

**[00:26:32]** It's you and I. It's what we can do with

**[00:26:34]** this technology. There's a new role, and

**[00:26:36]** it's getting talked about more and more

**[00:26:37]** and more by top engineers. This new role

**[00:26:40]** is called agentic engineering, the

**[00:26:42]** ability to build these kind of

**[00:26:44]** pseudo-living intelligence systems,

**[00:26:46]** right? That's what we're doing here.

**[00:26:48]** We're building systems that build

**[00:26:50]** systems, and that's the key idea inside

**[00:26:53]** of Tactical Agent Coding. We ask the

**[00:26:55]** question, what if your code base could

**[00:26:57]** ship itself? And we build the system

**[00:27:00]** that builds the system. You don't want

**[00:27:02]** to be working on your application

**[00:27:03]** anymore. If you're still doing this,

**[00:27:06]** you're wasting time. I'll just be really

**[00:27:07]** blunt with you. Someone has to. Instead,

**[00:27:09]** you work on the agentic system, the

**[00:27:12]** system that builds the system. This is

**[00:27:14]** what matters now. All the engineers

**[00:27:16]** getting the highest leverage, they're

**[00:27:18]** doing things like controlling their

**[00:27:20]** agent harness. They're controlling the

**[00:27:22]** core four, context model prompt tools.

**[00:27:25]** They're making it safe, secure. They're

**[00:27:27]** locking down the bash tool. They're

**[00:27:28]** adding more agents. They're adding

**[00:27:30]** custom agents. And then they're

**[00:27:32]** orchestrating their agents. What are

**[00:27:33]** they doing? They're operating on the

**[00:27:35]** agentic layer of their code base, the

**[00:27:38]** agentic system. They're not operating on

**[00:27:40]** the application. This is low-leverage

**[00:27:42]** activity. You can prompt against your

**[00:27:44]** primary code base and fix things one-off

**[00:27:46]** super super slowly over and over and

**[00:27:48]** over, waste all your time. That's fine.

**[00:27:50]** You can do that. If that's you, click

**[00:27:52]** away. The video's done. You know, GG.

**[00:27:54]** Good to see you.

**[00:27:55]** But um for everyone else that

**[00:27:56]** understands that we're in the age of

**[00:27:59]** agents. This is the highest leverage

**[00:28:01]** opportunity that's ever existed for us

**[00:28:03]** engineers. And everyone's so afraid that

**[00:28:06]** vibe coders and their mom and their

**[00:28:08]** brother are going to take away

**[00:28:09]** engineering jobs. Guys, that's just not

**[00:28:11]** true, okay? Vibe coding is the floor.

**[00:28:14]** Agentic engineering is the ceiling that

**[00:28:16]** no one has even imagined the

**[00:28:18]** capabilities of yet. If you're

**[00:28:20]** interested in advanced agentic

**[00:28:22]** engineering so powerful that your code

**[00:28:23]** base runs itself, this course is for

**[00:28:24]** you. All that to say, I'm going to be

**[00:28:26]** adding this code base. Uh this is a full

**[00:28:29]** kind of version of the code base where

**[00:28:31]** I'll be sharing all the verifier

**[00:28:33]** specialists, not just the generic

**[00:28:35]** verifier. And I'll also be sharing my

**[00:28:38]** GPT image to image generation skill with

**[00:28:40]** you there. In fact,

**[00:28:42]** I'll be honest with you, the additional

**[00:28:44]** members-only code bases that you're

**[00:28:45]** going to get inside of Agentic Curation

**[00:28:48]** is just a trick to get you inside the

**[00:28:50]** course. And by trick, I mean the real

**[00:28:51]** value is in the lesson. So, let me make

**[00:28:54]** this super clear. There's been confusion

**[00:28:55]** about this in the past. There are two

**[00:28:56]** courses here, Tactical Agenda Coding and

**[00:28:59]** Agenda Curation. If you want the full

**[00:29:01]** verify agent, you need to get both of

**[00:29:03]** these. You need to get Agenda Curation.

**[00:29:04]** If you think it's too much, if you think

**[00:29:06]** it's too expensive, it's probably not

**[00:29:08]** for you, okay? And that's okay, all

**[00:29:09]** right? Don't complain in my comment

**[00:29:10]** section. If it's not for you, it's not

**[00:29:12]** for you. And on that note, there's a

**[00:29:14]** full no questions asked 3-day refund. If

**[00:29:16]** this is not for you, if you don't get

**[00:29:17]** value, you can get a refund by lesson

**[00:29:19]** four of Tactical Agenda Coding. I don't

**[00:29:22]** want you in here if you don't want to be

**[00:29:23]** in here, okay? This is not a ploy or

**[00:29:24]** some scam. This is serious agentic

**[00:29:26]** engineering. I've been with the

**[00:29:28]** Generative AI industry since the

**[00:29:29]** beginning and I'm going to be here until

**[00:29:31]** it's all over. And so, eight lessons in

**[00:29:33]** the first course and then six lessons in

**[00:29:35]** the second course. We talk about big

**[00:29:36]** hitting ideas, agentic prompt

**[00:29:38]** engineering, building custom agents. We

**[00:29:40]** talk about multi-agent orchestration,

**[00:29:42]** agent experts, and then the code base

**[00:29:43]** singularity. The moment you want to

**[00:29:45]** strive toward where your agents can run

**[00:29:47]** your code base better than you can.

**[00:29:48]** Here's what the course looks like. Let

**[00:29:49]** me just go ahead and show you this. Once

**[00:29:50]** you sign up, you'll get access to all

**[00:29:52]** the lessons like this. Tactical Agenda

**[00:29:54]** Coding on the top, Agenda Curation on

**[00:29:56]** the bottom. And then you'll be able to

**[00:29:57]** click into member assets. And here

**[00:30:00]** you're going to have access to premium

**[00:30:02]** multi-agent orchestration systems that

**[00:30:04]** we've been working on, some on the

**[00:30:05]** channel and some that you haven't seen.

**[00:30:07]** So, these are all here. I'm going to be

**[00:30:09]** adding the verify agent as a fourth

**[00:30:12]** member only asset for you here. And once

**[00:30:14]** again, you want both courses to gain

**[00:30:16]** access to that. Enough pitching. Again,

**[00:30:18]** I'm going to have a basic version of

**[00:30:20]** this on my GitHub repo for you to check

**[00:30:21]** out. The core ideas are going to be

**[00:30:23]** there for you as well, all right? So, I

**[00:30:25]** hope this all makes sense. This is just

**[00:30:27]** one more reason to own your agent

**[00:30:29]** harness, okay? The number of custom

**[00:30:31]** agents, specifically the number of

**[00:30:33]** custom agent harnesses I'm building in

**[00:30:35]** 2026 is growing very, very rapidly. I

**[00:30:38]** mean, it's catching up with the number

**[00:30:39]** of skills, prompts, and custom agents

**[00:30:41]** I'm building, which is a crazy thing to

**[00:30:42]** say. It's because I'm getting full

**[00:30:44]** control over the experience that I'm

**[00:30:47]** having with my agents. And this comes

**[00:30:49]** down to, once again, two things: trust

**[00:30:52]** and scale. I said it at the end of 2025,

**[00:30:54]** 2026 is the year of trust. Do you trust

**[00:30:57]** your agents to do what you ask them to?

**[00:30:59]** And then, how much? At what scale?

**[00:31:02]** That's what we're dialed into here. This

**[00:31:04]** is just one of many ways you can scale

**[00:31:06]** your compute to scale your impact. The

**[00:31:08]** verifier agent is a very unique agent,

**[00:31:11]** though. Don't ignore this. Don't skip

**[00:31:13]** over this. Dial into this. Really think

**[00:31:15]** through this with your agents. The

**[00:31:16]** verifier sits at a very important middle

**[00:31:18]** ground between trust and scale. Most

**[00:31:21]** agents increase trust or scale, not

**[00:31:23]** both. The verifier does both by

**[00:31:25]** validating the claims that your primary

**[00:31:28]** agent has done in an atomic way and then

**[00:31:30]** helping you improve it with every prompt

**[00:31:33]** it writes. What could it not verify?

**[00:31:34]** What feedback does it need? What does it

**[00:31:36]** need from you? This feedback forces you

**[00:31:39]** out the loop. It forces you to template

**[00:31:41]** your engineering into the fabric of your

**[00:31:44]** agent harness. Where are we going on the

**[00:31:45]** channel? What's next? As you can tell,

**[00:31:47]** it's these two things. The winning

**[00:31:49]** formula is often much more simple and

**[00:31:52]** less hype-filled than you realize. All

**[00:31:54]** the top performers do two or three

**[00:31:56]** things over and over and over and over.

**[00:31:59]** We're increasing the trust we have in

**[00:32:00]** our system and we're scaling the

**[00:32:02]** out of our agents. That's it. That's

**[00:32:04]** what we're going to do on this channel

**[00:32:05]** for the rest of the year. If that

**[00:32:06]** interests you, like, subscribe. To be

**[00:32:09]** super concrete, there is a big hole in

**[00:32:11]** everyone's agent right now, and that

**[00:32:14]** hole is

**[00:32:16]** the bash tool. This is the most

**[00:32:18]** dangerous tool every engineer is running

**[00:32:20]** right now, and it is going to cause

**[00:32:22]** massive cataclysmic damage at some point

**[00:32:25]** to you. So, we're going to get ahead of

**[00:32:26]** that. Again, make sure you like,

**[00:32:28]** subscribe so you don't miss that video.

**[00:32:30]** We're going to be talking about agentic

**[00:32:32]** security, and I'm not talking about

**[00:32:33]** prompt injection. I'm talking about

**[00:32:35]** damage from within, damage from systems

**[00:32:37]** that you think you trust, but you don't,

**[00:32:40]** right? And again, this focuses on our

**[00:32:42]** trust theme. You know where to find me

**[00:32:44]** every single week. Stay focused and keep

**[00:32:48]** building.
