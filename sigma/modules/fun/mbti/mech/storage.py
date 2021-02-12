"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

mbti_list = [
    'estj',
    'esfj',
    'istj',
    'isfj',
    'estp',
    'esfp',
    'istp',
    'isfp',
    'entj',
    'entp',
    'intj',
    'intp',
    'enfj',
    'enfp',
    'infj',
    'infp'
]

mbti_chart = {
    'estj':	[3, 4, 4, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    'esfj':	[4, 5, 4, 3, 4, 2, 4, 4, 4, 3, 2, 2, 3, 2, 3, 3],
    'istj':	[4, 4, 5, 3, 4, 3, 3, 5, 3, 3, 4, 3, 3, 3, 4, 4],
    'isfj':	[2, 3, 3, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 3],
    'estp':	[3, 4, 4, 4, 5, 3, 4, 3, 4, 5, 3, 3, 4, 3, 2, 2],
    'esfp':	[3, 2, 3, 4, 3, 3, 4, 2, 4, 2, 4, 2, 5, 4, 3, 3],
    'istp':	[2, 4, 3, 4, 4, 4, 3, 3, 3, 3, 3, 4, 4, 3, 4, 2],
    'isfp':	[3, 4, 5, 4, 3, 2, 3, 3, 1, 4, 2, 3, 4, 3, 4, 3],
    'entj':	[3, 4, 3, 3, 4, 4, 3, 1, 4, 4, 4, 5, 2, 3, 3, 3],
    'entp':	[3, 3, 3, 3, 5, 2, 3, 4, 4, 4, 4, 5, 4, 4, 4, 4],
    'intj':	[3, 2, 4, 3, 3, 4, 3, 2, 4, 4, 4, 4, 2, 4, 3, 3],
    'intp':	[3, 2, 3, 3, 3, 2, 4, 3, 5, 5, 4, 4, 4, 3, 3, 4],
    'enfj':	[3, 3, 3, 3, 4, 5, 4, 4, 2, 4, 2, 4, 4, 5, 4, 5],
    'enfp':	[3, 2, 3, 3, 3, 4, 3, 3, 3, 4, 4, 3, 5, 5, 4, 5],
    'infj':	[3, 3, 4, 4, 2, 3, 4, 4, 3, 4, 3, 3, 4, 4, 4, 4],
    'infp':	[3, 3, 4, 3, 2, 3, 2, 3, 3, 4, 3, 4, 5, 5, 4, 4]
}

mbti_overview = {
    'p1': 'Myers-Briggs Type Indicator (MBTI) is a self-report inventory analysis based on the work of Isabel Myers '
          'and mother Katherine Briggs, inspired by Carl Jung’s theory of personality types.',
    'p2': 'This self-report inventory takes into account one’s likes, dislikes, strengths, weaknesses, '
          'possible career preferences, as well as compatibility with other personality types. Such information '
          'provides insight into methods for self-actualization and personal development.',
    'p3': 'Each of the sixteen MBTI personality types are comprised of a combination of eight cognitive functions, '
          'originally developed by Jung. These eight functions are crucial to understanding how one interacts with '
          'both internal and external stimuli, and are beneficial to know as a tool to assist in further analysis and '
          'consideration of how one operates. '
}

mbti_types = {
    'enfj': {
        'stack': 'fe-ni-se-ti',
        'p1': 'The FeNi is an expert relationship builder. Through Fe they can sense and assess where someone else is '
              'at in life or a certain situation. This may allow them to share in part of a friend’s feelings as '
              'their friend describes a situation they feel particularly strongly about. The FeNi will feel true '
              'indignation, joy, anger, etc. on behalf of others, making them master empathizers. Those around the '
              'FeNi will typically describe them as warm, caring people, and great friends.',
        'p2': 'FeNi’s use their Ni to intuitively know what needs to be done before it may even become a real issue. '
              'They tend to exhibit a natural foresight, anticipating needs 10 steps before others do. come from a '
              'perspective of looking 10 steps ahead of others, and can see the need before others do. They might '
              'even feel that people don’t appreciate what they do because they do something before the need is '
              'actually there. They might also refrain from taking an action they know someone needs because they '
              'don’t want to seem presumptuous. Because FeNi’s enjoy helping people and get energy from meeting '
              'people’s needs, FeNi individuals should be careful to surround themselves with good-willed, '
              'honest people so as to not “give” themselves to death.',
        'p3': 'The FeNi spends a good deal of their internal thought life thinking about relational issues—how their '
              'actions affect others and how they feel about what others said to them. They often realize after the '
              'fact that something they said could have been taken in a way they did not intend, which can cause them '
              'to worry that they might have unintentionally hurt or offended someone. They spend a lot of time '
              'thinking about future possibilities like their goals and aspirations. They might not think about these '
              'things in a step-by step way. Rather, they want to explore different possibilities of where their '
              'goals and interests might lead them. '
    },
    'enfp': {
        'stack': 'ne-fi-te-si',
        'p1': 'NeFi’s are constantly chasing new shiny ideas and studying fresh topics of interest. They derive '
              'satisfaction from learning about a huge variety of topics so they can use the information to fuel '
              'their ideas. The more diverse their learning and exploring is, the more likely it is that they can '
              'find a unique solution to a problem by pulling from their library of knowledge or understanding.',
        'p2': 'NeFi’s are extremely self-aware and spend a good deal of time on self-reflection. They are very '
              'concerned with the depth and nuances of their values system and spend a large amount of their mental '
              'space clarifying, sifting, and refining their beliefs. This process can be very connected to deep '
              'emotions for NeFi’s. They might find themselves laughing or crying at the beauty of a seemingly random '
              'object that has meaning to them, while bystanders who notice their reaction might be quite confused at '
              'their sudden outburst. For some NeFi’s, their emotions run so deep that there have to have been a lot '
              'of feelings building under the surface for quite some time before they will burst forth. They tend to '
              'seek out things (movies, books, etc.) that will engage their emotions, because following characters '
              'they care about through an emotional journey can be very rewarding for them.',
        'p3': 'The NeFi’s instinct is to achieve inner harmony by remaining true to themselves, their own values, '
              'and minimizing the influence that external factors (societal expectations, and maybe even the opinions '
              'of friends and family) have on their values. They may love discussing their values with others, '
              'as long as they are able to remain true to themselves while doing so.',
        'p4': 'NeFi’s find their own principles to be trustworthy and valuable, and are inherently skeptical of  '
              'others that try to impose on them. If something does not line up with their beliefs, they cannot act '
              'in accordance with it. To go against their own values is to cause inner discord, which NeFi’s can’t '
              'tolerate for long. '
    },
    'entj': {
        'stack': 'te-ni-se-fi',
        'p1': 'TeNi’s are very goal-oriented and results-driven. When they’re at their best, you aren’t likely to see '
              'them continue with an inefficient method for long. They tend to dislike getting into the dirty details '
              'of implementation and are likely to delegate as much as possible to others. It’s very obvious to a '
              'TeNi what is or isn’t going to work, and it can be frustrating when others don’t see solutions as '
              'obviously as they do. TeNi’s may be accused of being bossy or critical at times, but it’s important to '
              'note that they typically won’t bother correcting someone unless they value that person and/or their '
              'work. Although people might complain about the bossiness of a TeNi, the truth is that those around '
              'them would be usually be lost without their effective leadership.',
        'p2': 'Although TeNi’s are very social people, they are not afraid of being disliked in most cases. They '
              'don’t shy from necessary confrontation and when it comes to interpersonal conflict, they are apt to '
              'want to resolve issues in a quick, efficient manner and then move on with life. Only when they feel '
              'someone has wronged them or wounded them very deeply will they feel the need to cut people out of '
              'their life. In most instances, they prefer to resolve an issue and move on, without lingering too much '
              'in any emotional aspects of conflict.',
        'p3': 'TeNi’s have a deep internal world that is often hard for them to put into words or share with others. '
              'Ni is their main source of creativity. They are very intuitive and can often see all the possibilities '
              'for how a particular situation will play out. They are then able to analyze all the options and refine '
              'them down until they arrive at what they feel is the most likely one. Their inner world is constantly '
              'shifting and changing and analyzing different aspects of things. When they make plans or have a goal '
              'in mind, they are naturally able to skip ten steps ahead to see how it might turn out. '
    },
    'entp': {
        'stack': 'ne-ti-fe-si',
        'p1': 'NeTi’s are constantly chasing new shiny ideas and studying fresh topics of interest. They derive '
              'satisfaction from learning about a huge variety of topics so they can use the information to fuel '
              'their ideas. The more diverse their learning is, the more likely it is that they can find a unique '
              'solution to a problem by pulling from their library of knowledge. They are commonly known as '
              'polymaths, or renaissance men/women because of the variety of topics they learn about. They generally '
              'prefer to obtain competence in many areas rather than mastering just one skill or area of expertise.',
        'p2': 'NeTi’s get their ideas from the world around them and their ideas usually flow best when they have '
              'someone to bounce ideas off of. This is the nature of Ne and other external functions (denoted by the '
              'lowercase “e”) - they need interaction with the world to function optimally. This is a double-edged '
              'sword, as the outside world can also be highly distracting. Because of this, they tend to need '
              'alternating stages of input and output.',
        'p3': 'NeTi’s tend to be curious about people, but having to constantly care for others can drain them '
              'quickly. They love studying people and brainstorming with them, but their default is often to try and '
              'problem-solve for people when they’re upset rather than only listening to them. It can take some '
              'direct instruction from others before the NeTi learns what is appropriate in terms of responding to '
              'others who are in emotional pain. They may also start to feel uncomfortable around overly emotional '
              'people, and can have a strong desire for the other person to just feel better so things can be normal '
              'again.',
        'p4': 'NeTi’s are constantly taking in information and turning it over in their minds, looking at it from '
              'every angle and thinking about how it relates to everything else they’ve learned. They regularly ask '
              '“how does this work?” and “why is it like this?”  as their Ti filters and processes their discoveries '
              'to separate out what is useful or not useful, accurate or not accurate. '
    },
    'esfj': {
        'stack': 'fe-si-ne-ti',
        'p1': 'FeSi uses Fe to “read” the vibes of everyone in the room and is constantly keeping tabs on what '
              'everyone seems to be thinking and feeling. They subconsciously take in all this information, '
              'and make most of their choices based on this info, which essentially boils down to, “What can I do '
              'that will benefit the most people?” At the same time, the FeSi also uses their own mannerisms, '
              'expressions, emotions, and capabilities to influence and help others around them. When the FeSi gets '
              'good vibes, feelings, or a sense of something that sparks their interest from another person or group '
              'of people, they build on that expression and mirror it back to the person or group.',
        'p2': 'FeSi’s tend to be especially intelligent when it comes to reading facial expressions and body '
              'language. When they scan the room, they subconsciously take in the “aura” or “feeling” that radiates '
              'from each individual person. In the mind of an FeSi, this process categorizes the “feeling” gleaned '
              'from each person and notes the person’s facial expression, gesticulations, body placement, '
              'etc. and stores them away to be accessed and pulled from later.',
        'p3': 'FeSi’s are very concrete inside—they have a sense internally that their world is very black and white; '
              '‘right’, and ‘wrong’. Because of this, FeSi’s can be incredibly hard on themselves. They tend to set '
              'very high standards for themselves, because they believe that anything less is unacceptable. FeSi’s '
              'can use this to their advantage to create things with excellence, but they should be careful not to '
              'get so caught up in it that they don’t actually put anything out there because they feel it isn’t good '
              'enough, or become so focused on making things perfect that they lose sight of what actually matters. '
    },
    'esfp': {
        'stack': 'se-fi-te-ni',
        'p1': 'SeFi’s are all about in-the-moment, tangible, concrete, real world experiences and perceptions, '
              'and how they can connect their physical surroundings to their shifting, mystical inner world. It’s '
              'possible that those with strong Se are the only people who truly live ‘in the moment’, in a sense. '
              'They view the world as a solid force, and prefer to take in information in a concrete, solid way. '
              'Because they do not experience solidity within themselves, they seek that stability in the world '
              'around them.',
        'p2': 'SeFi’s especially feel that every moment should be spend on something worthwhile and fun, and doing '
              'anything they view as ‘work’ is arduous and tedious, even if it’s work they enjoy. They are all about '
              'having fun and experiencing new things, so even enjoyable work is rarely a favorite activity for them. '
              'They want to be able to do exactly what they want to do, the moment they think of doing it. Anything '
              'that hinders that freedom is a frustrating block to their Se.',
        'p3': 'While they can be great listeners, SeFi’s really enjoy doing things with people as a means of getting '
              'acquainted. They crave thrill and adventure and need to be engaged with the world around them. '
              'Exploring nature, getting involved in physical sports, or getting their hands dirty and doing things '
              'in the physical world is very cathartic for them.',
        'p4': 'At their best, SeFi’s are masters of self-care and great at putting healthy boundaries in place. They '
              'are empathetic people, so they see the needs of others and want to take care of them when they can. '
              'However, healthy SeFi’s know that they cannot effectively care for others unless they first care for '
              'themselves. They know their limits and aren’t usually afraid of saying ‘no’ when they aren’t able to '
              'do something or fit something into their lives. '
    },
    'estj': {
        'stack': 'te-si-ne-fi',
        'p1': 'TeSi’s are generally very organized people. This is not to say they’re all perfectly tidy, but when it '
              'comes to something that matters, they plan, organize, and execute their plans in a very linear '
              'fashion. When they put their all into a project and have the right tools and resources, you can be '
              'sure it will be very well executed.',
        'p2': 'TeSi’s are great at seeing areas for improvement in people’s lives. Because highly detailed systems '
              'naturally make sense to them, they may see a problem someone is having and try to help the person '
              'implement their own system as a solution. When they’re younger, they might try to apply their '
              'solutions to any potentially relevant problem they come across, thinking, “If it works for the me, '
              'of course it should work for the person I’m helping!” As they gain more experience in life, '
              'they learn to recognize when their help is welcome and where their solutions are actually a good fit, '
              'and they become a lot more strategic about the way they help people.',
        'p3': 'TeSi’s tend to have very high standards for themselves, which can cause them to focus on where they '
              'feel they’re falling short, even though those around them rarely demand the near-perfection they '
              'demand of themselves. Because they can be very driven and often end up in leadership roles where '
              'they’re the pioneer, it can get exhausting if they’re in a role where most of what they hear is '
              'negative feedback. Being a leader causes all their flaws to become more visible, and the perception '
              'most people have of TeSi’s is that they have no feelings at all. This can cause employees and even '
              'family members to be unnecessarily harsh in the way they speak to and about TeSi’s. '
    },
    'estp': {
        'stack': 'se-ti-fe-ni',
        'p1': 'SeTi’s have a strong need to be engaged in physical activity and DOING stuff in a tangible way, '
              'ideally being able to go as far as their physical limits allow and not having to interrupt the flow of '
              'the activity.',
        'p2': 'SeTi’s need a certain level of impulsiveness in life to be happy. While they don’t absolutely abhor '
              'schedules, it does get irritating for them when a schedule becomes more important than doing the '
              'things a schedule is supposed to allow time for. They also might break the rules from time to time, '
              'but not necessarily to rebel or make a point. They simply don’t think in terms of rules and '
              'procedures. Their focus is on actions that will accomplish specific things.',
        'p3': 'SeTi’s really enjoy doing things with people as a means of getting acquainted. They crave thrill and '
              'adventure. Exploring nature, getting involved in physical sports, or getting their hands dirty and '
              'doing things in the physical world is very cathartic for them. The Se side of an SeTi makes them value '
              'beauty very highly, and they are likely to seek out beautiful, serene surroundings, especially in '
              'nature. Their surroundings have a strong influence on them, and they are very aware of their physical '
              'environment.',
        'p4': 'SeTi’s are excited about the here and now of what is going on around them. They are very present, '
              'and might find it difficult to plan far into the future. They are so fully present in the moment that '
              'the current situation they find themselves in feels like it’s their whole world. If you were to ask an '
              'SeTi what their life is like, they may tell you about their current circumstances rather than the big '
              'picture. '
    },
    'infj': {
        'stack': 'ni-fe-ti-se',
        'p1': 'NiFe’s tend to have a rather large “working memory,” meaning that they can retain active consciousness '
              'of a large number of facts or details for immediate use. In the short term, they can have a remarkably '
              'accurate memory showing a great attention to detail, while still retaining the big picture. However, '
              'if they spend too much time trying to hold multiple perspectives and a wide array of details in their '
              'mind, they will suffer from internal overstimulation; this can even lead to moments of panic or '
              'feeling trapped inside of one’s head. It can also be a huge killer of the NiFe’s natural creativity.',
        'p2': 'The presence of Fe in an NiFe’s life is often experienced as a blessing and a curse. When they sense '
              'the emotions of other people, Ni’s vague, impressionistic nature often means that they don’t always '
              'clearly perceive origins and reasons for their emotional impressions. This is especially true for '
              'young NiFe’s who may not be able to clearly define why they dislike being around certain people or put '
              'in certain situations. It is the development of Ti  that allows them to retrace the steps that Ni '
              'traversed subconsciously.',
        'p3': 'They overwhelmingly feel that their inner world is vastly more fascinating and colourful than the '
              'world around them, and they struggle to convey anywhere near the level of detail, beauty, '
              'or simply the humor of what they’re experiencing in their mind in a way that does it justice. Too much '
              'time being forced to engage with the real world can get really exhausting for NiFe’s. Finding ways to '
              'minimize this drain is a good way to allow them to focus their creative abilities on the things they '
              'are best at. '
    },
    'infp': {
        'stack': 'fi-ne-si-te',
        'p1': 'FiNe’s are masters of self-care and typically great at putting healthy boundaries in place. They are '
              'very empathetic people, so they see the needs of others and want to care for them. However, '
              'healthy FiNe’s know that they cannot effectively care for others unless they first care for '
              'themselves. They know their limits and aren’t usually afraid of saying ‘no’ when they aren’t able to '
              'do something or fit something into their lives.',
        'p2': 'FiNe’s are extremely self-aware and spend a lot of time on self-reflection. They are very concerned '
              'with the depth and nuances of their values system and spend a large amount of their mental space '
              'clarifying, sifting, and refining their beliefs. This process can be very connected to deep emotions '
              'for FiNe’s.',
        'p3': 'For some FiNe’s, their emotions run so deep that there have to have been a lot of feelings building '
              'under the surface for quite some time before they will burst forth. They tend to seek out things ('
              'movies, books, etc.) that will engage their emotions, because following characters they care about '
              'through an emotional journey can be very rewarding.',
        'p4': 'The FiNe’s driving instinct is to achieve inner harmony by remaining true to themselves, their own '
              'values, and minimizing the influence that external factors (societal expectations, and maybe even the '
              'opinions of friends and family) have on their values. After a lengthy discussion, FiNe’s need time by '
              'themselves to evaluate the conversation and consider what the other person said and how they might fit '
              'it into their value system.',
        'p5': 'FiNe’s have a world of theories that are swirling around at any given time, and it’s important for '
              'them to have time alone in order to develop them. Their best ideas will usually come when they have a '
              'sense of inner peace and enough inspiration. Many FiNe’s find mindfulness, meditation, or another form '
              'of intentional relaxation to be useful for obtaining peace. '
    },
    'intj': {
        'stack': 'ni-te-fi-se',
        'p1': 'NiTe’s have a very deep internal world. They are extremely intuitive and can often see all the '
              'possibilities for how a particular situation will play out. They are then able to analyze all the '
              'options and refine them down until they arrive at what they feel is the most likely one. They may even '
              'be able to use this to predict the future in a sense.',
        'p2': 'NiTe’s really like improving things. They tend to enjoy work where they get to combine their ability '
              'to see ten steps ahead with their drive to make things better and more efficient. Some examples could '
              'be engineering, product design, architecture, or the sciences. They also tend to be interested in '
              'solving big practical issues like pollution or overpopulation.',
        'p3': 'NiTe’s tend to be very deliberate about the choices they make and they like to do things with '
              'excellence when they’re working on something they care about. This means that doing the right work, '
              'they are extremely responsible and determined. With the wrong work, they may get irritable and '
              'apathetic about the way the job is done, or may focus too much on little details without being able to '
              'see what’s most important in the context of the big picture. It’s important that they gain the '
              'self-awareness needed to know the difference.',
        'p4': 'NiTe’s internal world has a certain intensity to it that they may feel is lost once it’s brought out '
              'through verbal communication. They tend to be more at ease communicating through images, sound, '
              'written word, or some other form of expression where they are able to explore the full depth of an '
              'idea and expand on it before presenting it to public scrutiny. They are also usually more interested '
              'in finding the meaning behind things than taking them at face value, which means they may take some '
              'time to process new opportunities or unusual circumstances they find themselves in. '
    },
    'intp': {
        'stack': 'ti-ne-si-fe',
        'p1': 'Ti is primarily concerned with learning. Not just gaining knowledge, but understanding complex things '
              'in a deep way. TiNe’s see the possibilities available using Ne, pick things apart into their smallest '
              'components so that each detail can be stored using Si, and then apply this information across a '
              'variety of situations using Ne.',
        'p2': 'TiNe\'s need to withdraw from the world often in order to process all of their observations. They '
              'often spend a significant amount of time searching for cognitive biases within themselves so they can '
              'remove them and therefore be more objective in their analyses.',
        'p3': 'TiNe’s have a world of theories that are swirling around at any given time, and it’s important for '
              'them to have time alone in order to develop them. Their best ideas will usually come when they have a '
              'sense of inner peace and enough input. Many TiNe’s find mindfulness, meditation, or another form of '
              'intentional relaxation to be useful for obtaining peace. As far as input goes, learning interestings '
              'things or having an intellectual conversation with someone are safe bets.',
        'p4': 'For the ideas that have had some time to percolate, the TiNe needs to have places for output. Whether '
              'it’s writing, speaking, teaching, building, designing, or something else, it’s important to have space '
              'to string together the things they’ve studied in a unique way. This can also help them to refine and '
              'perfect the expression of their ideas. While they may feel like they understand something fully in '
              'their head, and they often make great teachers, they may not be as adept at explaining things to '
              'others without previous practice. '
    },
    'isfj': {
        'stack': 'si-fe-ti-ne',
        'p1': 'Si is internal or introverted Sensing. It’s all about real-world experiences, and how 5-senses ('
              'seeing, hearing, tasting, seeing, smelling) affect people with Si. SiFe’s value their own experiences '
              'very highly, and typically have a very good memory or catalogue of details about them.',
        'p2': 'SiFe’s are generally pretty in touch with the world around them because of their high value for '
              'real-world, tangible experiences. They tend to take care of life’s daily needs very well through an '
              'organized schedule or a to-do list planned out in their heads. Because the to-do list in their head is '
              'being added to just as quickly as they check things off, they may feel that they haven’t accomplished '
              'much unless they are able to see tangible results from their efforts.',
        'p3': 'SiFe’s are very reliable and dependable, and they expect the same from others. It can be frustrating '
              'for them when they can understand and see the steps needed to complete a project, but others around '
              'them can’t seem to see the work and details that will be necessary - especially when it’s the people '
              'who they need help from in order to accomplish their goal.',
        'p4': 'SiFe’s also tend to have very high standards for themselves, which can cause them to focus on where '
              'they feel they’re falling short, even though those around them probably don’t demand the '
              'near-perfection they demand of themselves.',
        'p5': 'SiFe’s strong internal sense of right and wrong can color their sense of themselves, as they naturally '
              'see all the things they aren’t perfect at (because their mental to-do list is never complete), '
              'and all the steps needed to obtain perfection, which overwhelms them. Because SiFe’s can naturally '
              'focus on what still needs to be done, using Fe feedback from other people to understand what they are '
              'really like in the world is a valuable process that can help the SiFe see the areas they are already '
              'excelling in. '
    },
    'isfp': {
        'stack': 'fi-se-ni-te',
        'p1': 'At their best, FiSe’s are great at knowing themselves, as they spend a lot of time on self-reflection. '
              'They are very concerned with the depth and nuances of their values; they spend a large amount of their '
              'mental space clarifying, sifting, and refining their beliefs. This process can be very connected to '
              'deep emotions, and they might find themselves laughing or crying at the beauty of a seemingly random '
              'object that has meaning to them, while bystanders who notice their reaction might be quite confused at '
              'their sudden outburst.',
        'p2': 'FiSe’s tend to have an active imagination well into adulthood. Fi dominant types are very concerned '
              'with The Story of/behind various things. For example, they might see a large, sturdy tree and wonder '
              'how long it’s been there, trying to imagine the events it’s been around for, or who else sat in its '
              'shade, what wisdom might be attached to or inside of that tree, etc. They automatically look for '
              'meaning everywhere—in books, movies, a passing remark from a friend, a special cup they like to use, '
              'or even why that tree was planted in a particular place.',
        'p3': 'FiSe’s tend to be very earthy, and are drawn to the mysterious, intuitive aspects of the world around '
              'them because of their Ni. They are all about in-the-moment, tangible, concrete, real world experiences '
              'and perceptions, and how they can connect their physical surroundings to their shifting, '
              'mystical inner world.',
        'p4': 'FiSe’s are typically very creative. Se likes very tangible, 5-senses (sight, touch, taste, smell, '
              'sound) experiences, so creating art with their hands (i.e. playing an instrument, painting, drawing, '
              'sculpting, photography, etc.) is very gratifying to them. In creating tangible art, they get to put Fi '
              'and Se to use by expressing meaning in all kinds of real-world ways that other people can experience. '
    },
    'istj': {
        'stack': 'si-te-fi-ne',
        'p1': 'SiTe’s are a practical, strategic thinkers that love pulling the best out of people and projects. '
              'Whatever they decide to do, it will probably involve maximizing potential.',
        'p2': 'Si is all about real-world experiences. SiTe’s, often without noticing, pay a lot of attention to how '
              'things that engage their 5 senses (seeing, hearing, tasting, seeing, smelling) affect them. They value '
              'their own experiences very highly, and typically have a very good memory or catalogue of details about '
              'them. They tend to store their impressions of experiences rather than direct memories of the '
              'experiences themselves. They use this information to help them make the best decisions possible in the '
              'future.',
        'p3': 'Despite some popular stereotypes, SiTe’s do change their minds, though it might take longer for them '
              'than for other types. They often have a quirky sarcastic sense of humour and care deeply for those '
              'close to them, though they are far more likely to show their love in practical ways rather than being '
              'sappy and overly affectionate.',
        'p4': 'SiTe’s manage concrete practical information more easily than abstract concepts. Because they are '
              'linear thinkers, they naturally ask themselves “What is the next step?”, and because they are '
              'detail-oriented, they are often able to manage or design highly complex systems and highly detailed '
              'projects with incredible grace.',
        'p5': 'SiTe’s tend to have very high internal standards for themselves, which can cause them to focus on '
              'where they feel they’re falling short, even though those around them probably don’t demand the '
              'near-perfection they demand of themselves. At times they may even get fixated on doing things “right” '
              'according to the rules they’ve internalized about how the world works, and in their younger years it’s '
              'not uncommon for them to try to impose these rules on their kids or people they’re trying to help. '
    },
    'istp': {
        'stack': 'ti-se-ni-fe',
        'p1': 'TiSe’s like to focus on real world problems and often have a strong appreciation for mastery and doing '
              'things with excellence and beauty. They don’t just want to learn, they want to be able to do something '
              'with it. Although they like having time to think about things, having Se means they can bypass Ti and '
              'take physical action when it’s clear and needed in the moment.',
        'p2': 'TiSe’s often have a thrill-seeking side, and may enjoy sports, gambling, skydiving, bungee jumping, '
              'adventure travel or speeding down the highway in a sports car or on their motorcycle. TiSe’s are often '
              'perceived based on this side of them that loves adventure and needs thrilling new experiences, '
              'but what people often don’t see is the sharp mind behind it all.',
        'p3': 'TiSe’s are often willing to jump out on a limb and task risks where many others are not. With their Ti '
              'performing an analysis of the situation and their Ni predicting how things will play out in the '
              'future, they can take leaps with a degree of certainty and thrill that others simply don’t have.',
        'p4': 'TiSe’s love achieving mastery. They want to feel like they can produce something excellent time after '
              'time. When they experience something that’s been done with beauty and excellence, their Ni gives them '
              'hints at why it’s beautiful and what makes it well-crafted.',
        'p5': 'TiSe’s like for people to get to the point and say what they really mean. They might get irritated '
              'when they feel like they are expected to pay attention and do all the right things in social '
              'situations.',
        'p6': 'Their lack of interest in adhering to social norms and love of logic should not be interpreted to mean '
              'that they do not care about other people in their lives. They simply show that they care in a '
              'straightforward, problem-solving way. Many TiSe’s do care deeply about social issues and the welfare '
              'of their communities, they just don’t usually have the emotional stamina to be “touchy feely” with '
              'more than a handful of people who are close to them. '
    }
}

mbti_functions = {
    'fe': {
        'name': 'Extraverted Feeling',
        'p1': 'The process of extraverted Feeling often involves a desire to connect with (or disconnect from) others '
              'and is often evidenced by expressions of warmth (or displeasure) and self-disclosure.',
        'p2': 'The "social graces," such as being polite, being nice, being friendly, being considerate, and being '
              'appropriate, often revolve around the process of extraverted Feeling. Keeping in touch, laughing at '
              'jokes when others laugh, and trying to get people to act kindly to each other also involve extraverted '
              'Feeling.',
        'p3': 'Using this process, we respond according to expressed or even unexpressed wants and needs of others. '
              'We may ask people what they want or need or self-disclose to prompt them to talk more about '
              'themselves. This often sparks conversation and lets us know more about them so we can better adjust '
              'our behavior to them.',
        'p4': 'Often with this process, we feel pulled to be responsible and take care of others\' feelings, '
              'sometimes to the point of not separating our feelings from theirs. We may recognize and adhere to '
              'shared values, feelings, and social norms to get along. '
    },
    'fi': {
        'name': 'Introverted Feeling',
        'p1': 'It is often hard to assign words to the values used to make introverted Feeling judgments since they '
              'are often associated with images, feeling tones, and gut reactions more than words.',
        'p2': 'As a cognitive process, it often serves as a filter for information that matches what is valued, '
              'wanted, or worth believing in. There can be a continual weighing of the situational worth or '
              'importance of everything and a patient balancing of the core issues of peace and conflict in life\'s '
              'situations.',
        'p3': 'We engage in the process of introverted Feeling when a value is compromised and we think, "Sometimes, '
              'some things just have to be said." On the other hand, most of the time this process works "in private" '
              'and is expressed through actions.',
        'p4': 'It helps us know when people are being fake or insincere or if they are basically good. It is like '
              'having an internal sense of the "essence" of a person or a project and reading fine distinctions among '
              'feeling tones. '
    },
    'ne': {
        'name': 'Extraverted Intuition',
        'p1': 'Extraverted iNtuiting involves noticing hidden meanings and interpreting them, often entertaining a '
              'wealth of possible interpretations from just one idea or interpreting what someone\'s behavior really '
              'means. It also involves seeing things "as if," with various possible representations of reality.',
        'p2': 'Using this process, we can juggle many different ideas, thoughts, beliefs, and meanings in our mind at '
              'once with the possibility that they are all true. This is like weaving themes and threads together.',
        'p3': 'We don\'t know the weave until a thought thread appears or is drawn out in the interaction of '
              'thoughts, often brought in from other contexts. Thus a strategy or concept often emerges from the '
              'here-and-now interactions, not appearing as a whole beforehand.',
        'p4': 'Using this process we can really appreciate brainstorming and trust what emerges, enjoying imaginative '
              'play with scenarios and combining possibilities, using a kind of cross-contextual thinking.',
        'p5': 'Extraverted iNtuiting also can involve catalyzing people and extemporaneously shaping situations, '
              'spreading an atmosphere of change through emergent leadership. '
    },
    'ni': {
        'name': 'Introverted Intuition',
        'p1': 'Introverted iNtuiting involves synthesizing the seemingly paradoxical or contradictory, which takes '
              'understanding to a new level. Using this process, we can have moments when completely new, unimagined '
              'realizations come to us.',
        'p2': 'A disengagement from interactions in the room occurs, followed by a sudden "Aha!" or "That\'s it!" The '
              'sense of the future and the realizations that come from introverted iNtuiting have a sureness and an '
              'imperative quality that seem to demand action and help us stay focused on fulfilling our vision or '
              'dream of how things will be in the future. Using this process, we might rely on a focal device or '
              'symbolic action to predict, enlighten, or transform.',
        'p3': 'We could find ourselves laying out how the future will unfold based on unseen trends and telling '
              'signs.This process can involve working out complex concepts or systems of thinking or conceiving of '
              'symbolic or novel ways to understand things that are universal. It can lead to creating transcendent '
              'experiences or solutions. '
    },
    'se': {
        'name': 'Extraverted Sensing',
        'p1': 'Extraverted Sensing occurs when we become aware of what is in the physical world in rich detail. We '
              'may be drawn to act on what we experience to get an immediate result.',
        'p2': 'We notice relevant facts and occurrences in a sea of data and experiences, learning all the facts we '
              'can about the immediate context or area of focus and what goes on in that context. An active seeking '
              'of more and more input to get the whole picture may occur until all sources of input have been '
              'exhausted or something else captures our attention.',
        'p3': 'Extraverted Sensing is operating when we freely follow exciting physical impulses or instincts as they '
              'come up and enjoy the thrill of action in the present moment. A oneness with the physical world and a '
              'total absorption may exist as we move, touch, and sense what is around us.',
        'p4': 'The process involves instantly reading cues to see how far we can go in a situation and still get the '
              'impact we want or respond to the situation with presence. '
    },
    'si': {
        'name': 'Introverted Sensing',
        'p1': 'Introverted Sensing often involves storing data and information, then comparing and contrasting the '
              'current situation with similar ones.',
        'p2': 'The immediate experience or words are instantly linked with the prior experiences, and we register a '
              'similarity or a difference—for example, noticing that some food doesn\'t taste the same or is saltier '
              'than it usually is.',
        'p3': 'Introverted Sensing is also operating when we see someone who reminds us of someone else. Sometimes a '
              'feeling associated with the recalled image comes into our awareness along with the information itself. '
              'Then the image can be so strong, our body responds as if reliving the experience. The process also '
              'involves reviewing the past to draw on the lessons of history, hindsight, and experience.',
        'p4': 'With introverted Sensing, there is often great attention to detail and getting a clear picture of '
              'goals and objectives and what is to happen. There can be a oneness with ageless customs that help '
              'sustain civilization and culture and protect what is known and long-lasting, even while what is '
              'reliable changes. '
    },
    'te': {
        'name': 'Extraverted Thinking',
        'p1': 'Contingency planning, scheduling, and quantifying utilize the process of extraverted Thinking.',
        'p2': 'Extraverted Thinking helps us organize our environment and ideas through charts, tables, graphs, '
              'flow charts, outlines, and so on. At its most sophisticated, this process is about organizing and '
              'monitoring people and things to work efficiently and productively.',
        'p3': 'Empirical thinking is at the core of extraverted Thinking when we challenge someone\'s ideas based on '
              'the logic of the facts in front of us or lay out reasonable explanations for decisions or conclusions '
              'made, often trying to establish order in someone else\'s thought process.',
        'p4': 'In written or verbal communication, extraverted Thinking helps us easily follow someone else\'s logic, '
              'sequence, or organization. It also helps us notice when something is missing, like when someone says '
              'he or she is going to talk about four topics and talks about only three.',
        'p5': 'In general, it allows us to compartmentalize many aspects of our lives so we can do what is necessary '
              'to accomplish our objectives. '
    },
    'ti': {
        'name': 'Introverted Thinking',
        'p1': 'Introverted Thinking often involves finding just the right word to clearly express an idea concisely, '
              'crisply, and to the point.',
        'p2': 'Using introverted thinking is like having an internal sense of the essential qualities of something, '
              'noticing the fine distinctions that make it what it is and then naming it. It also involves an '
              'internal reasoning process of deriving subcategories of classes and sub-principles of general '
              'principles. These can then be used in problem solving, analysis, and refining of a product or an idea.',
        'p3': 'This process is evidenced in behaviors like taking things or ideas apart to figure out how they work. '
              'The analysis involves looking at different sides of an issue and seeing where there is inconsistency. '
              'In so doing, we search for a "leverage point" that will fix problems with the least amount of effort '
              'or damage to the system.',
        'p4': 'We engage in this process when we notice logical inconsistencies between statements and frameworks, '
              'using a model to evaluate the likely accuracy of what\'s observed. '
    }
}

mbti_compatibility = {
    'ENTJ x ENTJ': {
        'p1': 'The ENTJ x ENTJ pairing can be a dual for command, with potential for compromise in allowing both to '
              'lead together. This pairing could be beneficial for the fact that both enjoy spending time with people, '
              'expressing themselves logically, and following set plans of action.',
        'p2': 'Both individuals will need to make an effort to communicate patiently and thoughtfully toward the '
              'other, while still maintaining logical efficacy in their speech and actions. In conflict, this should '
              'be coupled with working together to find a mutually beneficial solution through considering the '
              'other\'s viewpoints when discussing an issue.',
        'p3': 'ENTJs are likely to trust the other when consistency, drive and enthusiasm are present in '
              'accomplishing goals and initiative in fostering the relationship.'
    },
    'ENTJ x ESTJ': {
        'p1': 'While there are commonalities between both the ENTJ and ESTJ with both as Te-dominant, it\'s important '
              'to note that ENTJ will be primarily looking for an intellectual connection with theorization, whereas '
              'ESTJ is driven toward concrete facts and statements.',
        'p2': 'At first, the ESTJ may see the ENTJ as unconventional, with vague communication. However, their novel '
              'viewpoint of situations will be a refreshing draw toward the other. The ENTJ is likely to see the ESTJ '
              'as traditional, structured and slight conformist.',
        'p3': 'The natural confidence of both types will be alluring to the other, where the ENTJ considers and '
              'pursues the "what if?" and ESTJ provides powerful stabilization to the dynamic. However, this '
              'confidence needs to be taken into consideration in communication, where there is likely to be conflict '
              'if not honed in.'
    },
    'ENTJ x ENTP': {
        'p1': 'The relationship between ENTJ and ENTP can be intense. They are both energetic, charismatic and '
              'intelligent. They both love a good debate. This is a good thing, because they will do a lot of it, '
              'while rarely taking offense to each other\'s ideas being challenged.',
        'p2': 'Each are likely to recognize the other as one that "speaks their language," connecting over shared '
              'interests in science, technology or, simply, passion for understanding how the world works. It is '
              'likely that both will find the other interesting and stimulating to discuss topics with based on a '
              'shared abstract style of communication. While there are these similarities, there is likely for '
              'miscommunication if details are not defined, which should be worked through together.',
        'p3': 'It\'s vital that each acknowledges the appreciation they have for one another, without becoming too '
              'emotional. More like a well-timed "I enjoyed this conversation with you" as recognition of affection.'
    },
    'ENTJ x ESTP': {
        'p1': 'ENTJ and ESTP are both very active types; they both like to take action on many things, albeit through '
              'different methods. ESTPs are likely to be seen by the ENTJ as one that immediately jumps into action '
              'and start trying things, where the ENTJ prefers to make a plan, find a method, and approach things from '
              'the best means. ESTP may become irritated by ENTJs method-seeking. ESTPs may see ENTJs as bound to '
              'rules and protocols, which can be perceived as restrictive.',
        'p2': 'While both share Se and Ni, potential conflict can arise from ESTP\'s Ti conflicting with ENTJ\'s Te '
              'and arguments can become heated and go-round in circles with Te putting value in facts that might seem '
              'completely irrelevant to the ESTP\'s Ti. This can spur quite a few arguments, as both types are '
              'particularly competitive when it comes to who is "right."'
    },
    'ENTJ x ENFJ': {
        'p1': 'ENTJ tends to be charismatic, direct and logic in their behavior while ENFJ is more warm, genuine and '
              'empathetic. ENTJs prefer to process logically, while ENTJs express themselves emotionally.',
        'p2': 'To communicate effectively, ENTJs should be encouraging, supportive and sensitive toward ENFJs and '
              'their emotions, whereas ENFJs should expect to engage in open discussion with ENTJs on their needs and '
              'ideas.',
        'p3': 'ENFJs will feel most connected to ENTJs when they display consideration and compassion for them and '
              'try to build a meaningful, personal connection. ENTJs will appreciate when ENFJ expresses themselves '
              'directly and actively participates in discussion and shares ideas with them.',
        'p4': 'It\'s important that ENTJs avoid pressuring ENFJs in addressing situations logically and instead '
              'appreciate and encourage their empathetic thinking, while ENFJs should appreciate ENTJs\' logical '
              'thinking and recognize their positive contributions as a way of healthy motivation.'
    },
    'ENTJ x ESFJ': {
        'p1': 'ESFJs tend to value social structure, whereas ENTJs are more likely to value logic. This can cause for '
              'the ESFJ to perceive ENTJs as insensitive or impatient, with the ENTJ seeing ESFJ as demanding or '
              'oversensitive.',
        'p2': 'This pairing could complement each other positively by learning from the other\'s strengths; ESFJs '
              'could learn from ENTJ to be more future-oriented and objectively approach problems, and ENTJ could '
              'learn from ESFJ how to handle social life more sensitively.',
        'p3': 'It is important for ESFJ to realize that ENTJs prefer for people to act consistently, so committing to '
              'your word is crucial. ENTJs should acknowledge that ESFJs are sympathetic people who care to help '
              'others, so look to steer away from resentment of their sociability or generosity.',
        'p4': 'ESFJs may use their tertiary Ne to deflect criticism or resist change, where ENTJ may use tertiary Se '
              'to defensively overemphasize competition or recognition. As resolve, ESFJs should remember that ENTJs '
              'are natural problem solvers and not to automatically take their advice as criticism. ENTJ should work '
              'to become more patient and supportive of the ESFJs efforts to resolve conflict that they may typically '
              'have difficulty navigating through.'
    },
    'ENTJ x ENFP': {
        'p1': 'ENTJ-ENFP pairing could complement each other well granted they are open to appreciating each other\'s '
              'strengths and be accepting of their differences. ENTJs can learn from ENFP to be more creative, '
              'easygoing and in touch with personal values rather than become too focused on external measures of '
              'success, whereas ENFPs can learn from ENTJ to be more focused and effective in reaching goals.',
        'p2': 'In maintaining the vitality of this pairing, both should recognize the importance of handling '
              'emotional conflict in a way that is mutually acceptable, with ENFPs approaching conflict more '
              'objectively and ENTJs learning to approach the situation with more sensitivity.',
        'p3': 'This pairing would benefit from finding a creative project that can be worked on together to bond '
              'through teamwork and combining strengths in complementary ways. Another way to build rapport is to '
              'spend more quiet time together discussing and sharing personal values and perspective.'
    },
    'ENTJ x ESFP': {
        'p1': 'ENTJ-ESFP pairing has potential to be beneficial were both types to recognize the value each bring to '
              'the dynamic through their differences.',
        'p2': 'ESFPs tend to be enthusiastic, spontaneous and adventurous, whereas ENTJs may have more difficulty '
              'letting go of planning or control. Balance can be achieved with ESFP helping ENTJ to maintain order and '
              'fulfill their responsibilities by being reliable and consistent, and ENTJ to understand ESFP tends to '
              'be more adaptable and responsive to their environment due to their dominant Se function.',
        'p3': 'ESFPs can learn from ENTJ to approach situations more objectively and work towards long-term goals, '
              'and ENTJs can learn from ESFP to become more in tune with themselves and develop greater value of '
              'interpersonal relationships.',
        'p4': 'This pairing can become stronger through both taking a greater interest in each other\'s passions or '
              'hobbies. It is encouraged to find an engaging physical/creative activity where both can complement the '
              'other\'s strengths and bond through teamwork and togetherness.'
    },
    'ENTJ x INTJ': {
        'p1': 'ENTJ-INTJ pairing can be mutually beneficial when both reach and acceptable compromise about social '
              'events or activities. ENTJs are action-oriented and more likely to involve themselves in external '
              'activities, whereas INTJs tend to keep to themselves unless pressured by outside forces. This can cause '
              'ENTJ to view INTJs as passive and INTJ to perceive ENTJs as controlling.',
        'p2': 'Both types can find compromise through ENTJ allowing INTJs their privacy and space without pressure, '
              'and INTJ realizing ENTJs need plenty of outside stimulation and being more willing to participate when '
              'able to.',
        'p3': 'Each type should support the other in their interests and become more open to each other\'s advice.'
              'ENTJs can help strengthen the dynamic through taking more time to learn about what fascinates the INTJ '
              'and helping them put ideas into action. INTJs can do the same through taking more of an interest in '
              'ENTJ\'s activities by using your analytical skills to aid them in achieving broader, more long-term '
              'views of their plans and actions.',
        'p4': 'In conflict, it is best to work toward communicating in a calm and reasonable way, taking a short '
              'break to process the situation objectively if things become to emotionally charged. It\'s important to '
              'not let problems ruminate unresolved for too long as this can forge a divide between you both.'
    },
    'ENTJ x ISTJ': {
        'p1': 'ENTJ-ISTJ dynamic has potential to be highly beneficial through combining strengths and working on '
              'improving weaknesses together. ENTJ could learn from ISTJs to become more reflective and careful about '
              'handling important details, and ISTJ could learn from ENTJs to be more focused on long-term goals and '
              'creative problem-solving.',
        'p2': 'Both types value competency and structure through Te high in each\'s function stack. However, ENTJs '
              'tend to be more action-oriented, which can be perceived as hasty by the ISTJ. ENTJs should understand '
              'that ISTJs need more time to process new information, so avoid pressing them to make changes too '
              'quickly. On the flip side, ISTJs should acknowledge that ENTJs like to solve problems creatively and '
              'efficiently, so try to be more open-minded to their methods and ideas.',
        'p3': 'In conflict, both ENTJ and ISTJ could benefit from learning to express dissatisfaction and negative '
              'emotions more constructively by putting themselves in the other\'s shoes to see their point-of-view. By '
              'changing the perspective of disagreements from that of a "problem" to an opportunity to know each other '
              'more deeply, both types can build a stronger bond with the other.'
    },
    'ENTJ x INTP': {
        'p1': 'ENTJ-INTP pairing can be mutually beneficial through learning from each other\'s strengths and being '
              'accepting of differences. ENTJs can learn from INTPs to analyze situations more carefully with greater '
              'attention to detail, while INTPs can learn from ENTJs to be action-oriented and more involved in the '
              'external world.',
        'p2': 'ENTJs should remember that INTPs need time to process information in their own time, so look to have '
              'more flexible expectations and not rush or pressure them into decisiveness. INTPs should keep in mind '
              'that ENTJs need more structure to feel at ease, so help to maintain order and fulfill responsibilities '
              'reliably.',
        'p3': 'In conflict, ENTJ and INTP should learn to communicate more openly with one another, so that problems '
              'are not left unresolved. Both types would benefit from learning to express or handle negative emotions '
              'in a constructive way, which would further enable open communication in this dynamic.',
        'p4': 'Finding a creative or strategic activity that can be enjoyed together would be a healthy way of '
              'building rapport and trust with one another.'
    },
    'ENTJ x ISTP': {
        'p1': 'ENTJ-ISTP pairing would benefit from taking into account the others\' preferences in interacting with '
              'their internal and external world. While both types are skilled problem solvers, ISTPs tend to resolve '
              'situations in a linear and deliberate way, while ENTJs tend to do so in a more conceptual and efficient '
              'way.',
        'p2': 'ISTPs could help strengthen this bond through using their analytical skills to complement the ENTJs '
              'endeavors, with ENTJs being more open to ISTPs advice and practical approach to situations as their '
              'greater affinity to certain details can help fill in what may have been overlooked.',
        'p3': 'Both types would benefit from growing in their communication skills to address situations in a calm '
              'and rational manner, as well as developing a stronger sense of trust to feel comfortable in sharing '
              'private thoughts and feelings with one another. ISTPs should not withdraw too quickly when conflict '
              'occurs and ENTJs should be mindful not to be too pushy or critical.',
        'p4': 'This pairing would find value in finding a leisurely project or challenge that can be worked on '
              'together so both can showcase their skills and strengths, helping to build closeness and/or intimacy in '
              'the process.'
    },
    'ENTJ x INFJ': {
        'p1': 'ENTJ-INFJ pairing has potential to be mutually beneficial through maintaining a non-judgmental '
              'perspective toward each other\'s differences and learning from the other\'s strengths. ENTJs can teach '
              'INFJs to be more effective in viewing situations in an objective manner, while INFJs can teach ENTJs to '
              'be more considerate and patient in understanding people and handling interpersonal relationships more '
              'effectively.',
        'p2': 'INFJs should realize that ENTJs are action-oriented people who value direct communication and '
              'efficiency, so consider being straightforward when it comes to needing time for yourself as well as '
              'finding compromise and resolving conflict in a calm and objective way. ENTJs should acknowledge that '
              'INFJs need time and space to process their experiences, so work to become more patient and considerate '
              'of their emotions and needs.',
        'p3': 'This dynamic would benefit from participating in fun, physical activities together, such as hiking or '
              'sports to become more in tune with each\'s Se. It is recommended to keep the competitive nature of '
              'these activities to a minimum so it can be more about quality time spent together and bonding over '
              'similar interests.'
    },
    'ENTJ x ISFJ': {
        'p1': 'ENTJ-ISFJ pairing could complement each other well through acceptance of differences and learning from '
              'each other\'s strengths. ENTJs could learn from ISFJs to be more practical and sensitive in handling '
              'relationships, while ISFJs could learn from ENTJs to be more assertive and open to new ideas or '
              'problem-solving methods.',
        'p2': 'ENTJs should acknowledge that ISFJs have their own structure and routine, so remember to respect their '
              'personal space and rituals. ISFJs should keep in mind that ENTJs approach situations with a need to be '
              'efficient, so be aware that their suggestions and advice should not always be seen as criticism. It is '
              'important for the ISFJ to speak up if it is felt the ENTJ is not respecting their needs or '
              'preferences.',
        'p3': 'During conflict, both types would benefit from learning to express dissatisfaction in a constructive '
              'and respectful way that can be more easily accepted by the other, since both tend to have difficulty '
              'handling negative emotions. Since ISFJs function better when relationships are harmonious and based on '
              'respect, ENTJs should try being more encouraging and supportive toward their counterpart. ISFJs should '
              'remember that ENTJs are not always in tune with their feelings and emotions, so allow time for them to '
              'process their thoughts or calm down when conflict becomes too elevated.',
        'p4': 'This pairing would benefit from coming to an acceptable compromise on how to maintain beneficial E/I '
              'balance in shared activities, so that neither feel neglected nor uncomfortable.'
    },
    'ENTJ x INFP': {
        'p1': 'ENTJ-INFP pairing could complement each other well through learning from the other\'s strengths and '
              'being more open to each other\'s advice or suggestions. INFPs could teach ENTJs to be more reflective '
              'and treat people more sensitively, while ENTJs could teach INFPs to be more organized and '
              'goal-oriented.',
        'p2': 'INFPs tend to be more spontaneous and individualistic than ENTJs, whereas ENTJs usually need more '
              'structure and routine. With that, ENTJs would benefit from realizing that INFPs are creative people who '
              'enjoy exploring novel ideas, and being more open-minded to exploring these ideas with them. INFPs '
              'should acknowledge that ENTJs tend to be driven and ambitious, so look to be more supportive and '
              'accepting of their endeavors.',
        'p3': 'In conflict, both types would benefit from learning to express negative emotions in a constructive way '
              'to best resolve relationship concerns. It\'s important that both ENTJ and INFP maintain open and direct '
              'communication (while remaining sensitive to the other\'s feelings) with each other to reduce the '
              'tendency for misunderstandings.',
        'p4': 'ENTJs should realize that INFPs tend to be empathetic people strongly connected to their emotional '
              'life, so be mindful of not judging them as being "oversensitive," and INFPs should acknowledge that '
              'ENTJs are not always well-versed in identifying with and expressing their emotional life, so look to '
              'approach them in a more calm and objective manner.'
    },
    'ENTJ x ISFP': {
        'p1': 'ENTJ-ISFP pairing are known to have "reverse compatibility" in that they share the same functions, but '
              'in reverse order. This has potential for a beneficial complement of each other, granted both are open '
              'to accepting help from the other in improving weaknesses.',
        'p2': 'ENTJs are very future-oriented, so ISFPs can benefit the relationship by working with them in '
              'achieving their goals and encouraging them to improve their work-life balance. On the other hand, ISFPs '
              'value creative expression and living life in the moment, so ENTJs could help strengthen this dynamic '
              'through taking an interest in their passions and encouraging them to develop toward their goals.',
        'p3': 'In conflict, ISFPs should approach ENTJs in a direct and calm manner about how they are feeling, while '
              'ENTJs should be mindful of their tone and word usage toward ISFPs so as to not come across as too harsh '
              'or overly critical. It is vital that problems are not left unresolved for too long, as this can cause '
              'undue withdrawal and possible resentment from both types.',
        'p4': 'This pairing would benefit from finding a physical or creative activity that can be done together to '
              'bond over teamwork and combine strengths in a complementary way.'
    },
    'ESTJ x ESTJ': {
        'p1': 'ESTJ-ESTJ pairing is a same-type relationship that has potential for mutual benefit, granted both '
              'people are mindful of reflecting back their weaknesses to the other. It is vital that both individuals '
              'maintain openness for improving together as a team through talking out concerns in a calm and concrete '
              'manner. With that, mapping out a clear and efficient method for resolving disagreements ahead of time '
              'will serve this pairing well in the long-term.',
        'p2': 'Since ESTJ tend to be very socially active, it\'s important that both individuals remember to take '
              'time to have alone time, so there is reduced risk over overextending themselves. Both people would also '
              'benefit from improving their emotional acuity and handling relationship concerns with more sensitivity, '
              'taking time to cool down and gather one\'s thoughts before engaging in difficult discussions.',
        'p3': 'For both individuals in this dynamic, actions speak louder than words. This means that both should '
              'ensure they are displaying both commitment in their words and actions. This pairing would benefit from '
              'setting mutual goals to strive for together, which will help strengthen trust and reliability toward '
              'one another.'
    },
    'ESTJ x ENTP': {
        'p1': 'ESTJ-ENTP pairing would benefit from becoming more understanding of the other\'s point-of-view. ESTJs '
              'can teach ENTPs to be more realistic and practical in conceptualizing and carrying out plans, while '
              'ENTPs can show ESTJs how to expand their perspective and become more flexible and present in the '
              'moment.',
        'p2': 'While ENTPs are abstract world thinkers and enjoy considering ideas and possibilities, ESTJs may be '
              'hesitant or resistant toward the unknown. This lends itself to the recommendation that ENTPs should '
              'recognize that ESTJs have a strong alignment toward order and predictability, so working to ensure '
              'dependability and consistency in their actions will be reassuring to their counterpart. All the while, '
              'ESTJs should understand that ENTPs are usually more easygoing and spontaneous, so look to be more '
              'open-minded to exploring ideas and experiences together with them.',
        'p3': 'Both types would benefit from being more sensitive to the other\'s needs and work toward expressing '
              'negative emotions in a constructive way, as both ESTJ and ENTP can become oversensitive to feeling '
              'incompetent in challenging situations. Being open to admitting weaknesses or mistakes will enable '
              'greater open communication and understanding between each other.'
    },
    'ESTJ x ESTP': {
        'p1': 'ESTJ-ESTP pairing would benefit from learning to appreciate their differences and utilize them in a '
              'complementary way; ESTPs could encourage ESTJs to open up more and relax -- to be more adventurous, '
              'while ESTJs could show ESTPs methods for planning and accomplishing goals more effectively.',
        'p2': 'Since both ESTJ and ESTP tend to be present-oriented, it is important that long-term goals are '
              'established in this dynamic. It is recommended that both work toward discussing concerns openly and '
              'work through decisions together.',
        'p3': 'In conflict, ESTJs can help resolve concerns through being patient in listening and understanding the '
              'ESTP\'s perspective, while ESTPs should work to address problems rather than avoid them or haphazardly '
              'move through them. Both types should work to better handle negative emotions and expression of '
              'dissatisfaction in a way that the other has expressed would be acceptable and understood.',
        'p4': 'This dynamic would benefit from sharing experiences together through exciting activities or hobbies, '
              'however both should be mindful of setting aside time for personal reflection so focus can ultimately be '
              'maintained on mutual goals and interests.'
    },
    'ESTJ x ENFJ': {
        'p1': 'ESTJ-ENFJ dynamic is coupled by mutual assertive behaviors and relatively strict expectations of '
              'people, where ENFJs expect people to honor social values and ESTJs expect consistent behavior from '
              'others.',
        'p2': 'ESTJs should understand that ENFJs are sympathetic individuals that care tremendously about the '
              'interest of others, so be mindful of any feelings of resentment toward their helpful, sociable or '
              'generous tendencies. ENFJs should acknowledge that ESTJs value competency, structure and consistency, '
              'so they should make an effort to mean what they say and say what they mean. In that, each would benefit '
              'from learning to express negative emotions in a constructive way, as both types can become accusatory '
              'when under duress, making it difficult to effectively resolve conflict.',
        'p3': 'Both types tend to be outgoing, becoming overly concerned with the external world. Each should make an '
              'effort to set aside time for personal reflection and prioritization, but also ensure that both are '
              'exploring new experiences and interests together to foster a greater connection.'
    },
    'ESTJ x ESFJ': {
        'p1': 'ESTJ-ESFJ pairing has potential for mutual benefit through focusing on common goals and helping each '
              'other by supplementing the other\'s weaknesses. ESTJ can show ESFJ how to handle criticism or '
              'challenging decisions with a more objective detachment, while ESFJ can teach ESTJ how to be more '
              'sensitive toward people and relationships.',
        'p2': 'Since both types tend to be present-oriented, it is important that there are mutual long-term goals '
              'established for progress toward improvement and personal development. This dynamic would benefit from '
              'experiencing new things and activities given both tend to enjoy the certainty of routine, structure and '
              'planning.',
        'p3': 'Both types tend to be detail-oriented and methodical when working through objectives, however have '
              'different personal priorities based on past experiences. These differences may lead each to see the '
              'other as stubborn or nitpicky about having things done a certain way. It is recommended that both types '
              'look to approach disagreement in a way that maintains focus on compromise, while still respecting '
              'individual differences in perspective.',
        'p4': 'ESTJ and ESFJ tend to be socially active types -- it is important that each set aside time for '
              'personal activities so as to not become overextended or exhausted.'
    },
    'ESTJ x ENFP': {
        'p1': 'ESTJ-ENFP pairing would benefit from each learning from the other\'s strongsuits and supplementing for '
              'their weaknesses. These two types have the same four main functions, albeit in different order, with '
              'ENFP leading with Ne and ESTJ leading with Te. ENFPs lean on their dominant Ne function in valuing '
              'exploration of novel ideas and possibilities, whereas ESTJ hones in on their dominant Te function '
              'through structure and order.',
        'p2': 'ENFPs should acknowledge that ESTJs need a lifestyle complemented by structure and routine, so it '
              'would be beneficial to help in maintaining order and being reliable in responsibilities. ESTJs should '
              'recognize that ENFPs are more spontaneous, adventurous and consider various possibilities, so learning '
              'to be more open and flexible toward new ideas and experiences would help bridge the gap between each '
              'other.',
        'p3': 'When conflict occurs, ESTJ and ENFP address the situation in very different ways. Both types would '
              'benefit from learning how to express their negative feelings in a way that the other would best '
              'understand to reduce misunderstanding. It is important that ESTJs understand ENFPs tend to be '
              'indecisive and conflict avoidant, whereas ENFPs should acknowledge that ESTJs usually struggle in '
              'situations where emotions run high; working around these sensitivities to find middle ground will help '
              'both types better resolve conflict together.'
    },
    'ESTJ x ESFP': {
        'p1': 'ESTJ-ESFP pairing has many differing factors, however both can find middle ground by learning from '
              'each other\'s strengths. ESFPs can teach ESTJs how to be more relaxed, understanding and accommodating '
              'in social situations, whereas ESTJs can teach ESFPs how to be more diligent and efficient in setting '
              'and pursuing goals.',
        'p2': 'Both types tend to be more present-oriented, so this dynamic would benefit from collaboration on '
              'long-term goals that can be worked toward together. Though, it is important to acknowledge that each '
              'type focuses on their own respective priorities, with ESTJs placing more value on effectiveness and '
              'efficiency in reaching goals, and ESFPs focus more on personal values to guide their behavior and '
              'actions.',
        'p3': 'ESTJs can help bridge the gap between each other through granting ESFPs the freedom to make decisions '
              'on their own and learn independently, and ESFPs can do so through helping ESTJs maintain order in daily '
              'life to keep things run smoothly.',
        'p4': 'This pairing would benefit from finding shared interests that can be enjoyed together, while still '
              'ensuring both set time aside for self-reflection and independent activities.'
    },
    'ESTJ x INTJ': {
        'p1': 'ESTJ-INTJ pairing has potential to be a strong match, with ESTJs remembering that INTJs are '
              'independent people needing their own privacy and space. INTJs should also acknowledge that ESTJs are '
              'action-oriented and prefer to stay "in motion."',
        'p2': 'Since each type has Te high in their function stack, both value logic and order. However, ESTJs tend '
              'to be more assertive in establishing and maintaining these values, while INTJs do so in a more private '
              'way. With that, both should remember that the other prefers structure in their own way and these '
              'differences should be respected through compromise and finding middle ground in navigating each '
              'other\'s preferences.',
        'p3': 'During conflict, ESTJs and INTJs tend to find challenge in emotional expression and management, so '
              'learning how to better handle emotions and being patient with the other as they do so will help resolve '
              'situations in a more constructive manner.',
        'p4': 'This dynamic can grow closer through participating in activities together where collaboration of '
              'skills can occur in a complementary way. It is recommended that both types make effort to recognize '
              'each other\'s accomplishments and support each other in such pursuits.'
    },
    'ESTJ x ISTJ': {
        'p1': 'ESTJ-ISTJ pairing share the same top four functions, which lends itself to similar strengths and '
              'weaknesses. With that, both types should be mindful of steering away from highlighting the other\'s '
              'vulnerabilities, and instead learn from the other\'s strengths for personal growth.',
        'p2': 'Each type has Te high in their function stacks, so both tend to place focus on stability and '
              'predictability in daily life, with preference toward well-established methods as indicated through '
              'shared their Si. Even though ESTJs and ISTJs prefer structure and routine, there may be differing views '
              'on what the "right" way is. Both types would benefit from maintaining awareness and respect for the '
              'other\'s boundaries, routines and values, as well as being more open to their counterpart\'s '
              'suggestions for improvement.',
        'p3': 'It is important for ESTJs to acknowledge that ISTJs need more personal time to process information and '
              'pursue their own interests, while ISTJs should be mindful of ESTJs\' action-oriented nature and '
              'consider being more open-minded to joining their activities.',
        'p4': 'By finding a mutually intriguing hobby to participate in together, this pairing can grow closer '
              'through collaboration and teamwork. Look to find an agreeable compromise on maintaining healthy balance '
              'in shared interests, while being open to new experiences to maintain excitement in the dynamic.'
    },
    'ESTJ x INTP': {
        'p1': 'ESTJ-INTP pairing can certainly benefit through learning from the other\'s strengths; INTPs can teach '
              'ESTJs to be more reflective and creative thinkers, while ESTJs can shine light on how to be more '
              'action-oriented and organized.',
        'p2': 'Since ESTJs tend to be more sociable and outgoing than INTPs, it is important for them to realize that '
              'INTPs are analytical people that tend to need more time to make decisions or take action. On the other '
              'hand, INTPs would benefit from acknowledging that ESTJs are action-oriented individuals, valuing '
              'efficiency and effective actions. This dynamic would benefit from granting each other enough space and '
              'independence to go about daily life in their own way.',
        'p3': 'Both ESTJs and INTPs tend to have difficulty handling emotions and sensitivities, so both should look '
              'to grow in how they express dissatisfaction or negative feelings constructively. It is recommended that '
              'both make an effort to communicate more openly with each other and share thoughts and ideas to foster a '
              'closer bond.'
    },
    'ESTJ x ISTP': {
        'p1': 'ESTJ-ISTP pairing would benefit from each type being more open to the other\'s advice and learning '
              'from their strengths. ESTJs can learn to become more relaxed and reflective from ISTPs, while ISTPs can '
              'learn organization and goal-planning techniques from ESTJs.',
        'p2': 'It is important for ESTJs to keep in mind that ISTPs are independent people, preferring less '
              'restriction in pursuits, so being more flexible toward their activity would be beneficial. ISTPs should '
              'recognize that ESTJs value structure and predictability, so work to be consistent and reliable in '
              'fulfilling responsibilities.',
        'p3': 'Both ESTJs and ISTPs can feel insecure about processing emotions, which can cause difficulty in '
              'resolving conflict. It is recommended that both types work to become more in touch with their true '
              'needs and feelings, and share their personal thoughts and concerns with the other in a constructive '
              'manner.',
        'p4': 'This dynamic can foster a greater sense of closeness through finding a fun, competitive or adventurous '
              'activity both can spend time together doing to build trust.'
    },
    'ESTJ x INFJ': {
        'p1': 'Sharing no common functions and inverted preferences, INFJs and ESTJs together can cover a wide array '
              'of perspectives and skill sets. Their approaches are widely different, which can allow for a dynamic '
              'and thoroughly-arranged lifestyle.',
        'p2': 'The biggest strength can also be their largest enemy if left unchecked. ESTJs are Te-Si dominant, so '
              'their lifestyle is dedicated towards what works and shouldn\'t change. ESTJs are very to-the-point '
              'types, and their communication style often aligns with that approach. INFJs should be prepared for the '
              'ESTJ\'s blunt communication style, and should work to not take it personally. Meanwhile, the ESTJ '
              'should keep in mind how their communication style could be taken by their INFJ partner. Likewise, the '
              'ESTJ should be aware of the INFJ\'s quiet and often compromising nature, and allow the INFJ time to '
              'effectively communicate their perspective. The INFJ should work to be okay voicing their perspective '
              'more regularly.',
        'p3': 'In a relationship setting, both types should be aware of the other\'s relationship to emotions. INFJs '
              'are feeling-dominant types, with aux-Fe. INFJs are often very aware of how things effect other people, '
              'and they care very deeply about harmony. INFJs must recognize that the ESTJ has inferior-Fi, but still '
              'has feelings. In order to ensure peace, the INFJ should be on the lookout for what the ESTJ values and '
              'cognizant of those values.'
    },
    'ESTJ x ISFJ': {
        'p1': 'ESTJ-ISFJ pairing has the opportunity to be successful, albeit a challenged pursuit due to the vastly '
              'different communication styles each type has. Each type has Sihigh in their function stack, which makes '
              'both inherently skilled at handling details; both respect prior experiences, however ISFJs guide their '
              'behavior through their own internal priorities and commitments that ESTJs may view as misguided or '
              'selfish. Beyond this, ISFJs\' auxiliary Fe lead them to be "people-pleasers" and they tend not to '
              'respond well to blunt criticism, whereas ESTJs dominant Te influence their assertive behavior and '
              'trouble in meeting other\'s emotional needs - ISFJs could see these ESTJ attributes as domineering and '
              'harsh.',
        'p2': 'This duo can bridge the gap in their intrinsic dispositions through mutual patience, active listening, '
              'and discretion in how each indulge in discussing their partner\'s life to others - look to forego '
              'sharing personal information about each with other people out of respect for their privacy. Beyond '
              'this, both types have varied social limits, so ISFJs should realize that ESTJs are social and enjoy '
              'interacting with their external environment and others frequently. ISFJs need privacy and more alone '
              'time, so ESTJs should work to spend more personal one-on-one time with their counterpart.'
    },
    'ESTJ x INFP': {
        'p1': 'ESTJ-INFP pair is complementary in that both share the same functions but in reverse '
              'order...ultimately viewing the world in completely different ways. While this can cause some friction, '
              'it does not imply that this pair is incompatible. In fact, this pairing could very well complement each '
              'other extremely well through supplementing each other\'s weaknesses via their individual strengths.',
        'p2': 'ESTJs should be mindful of the fact that INFPs may need a while to open up and talk about what is '
              'deeply set on their mind; look to be an attentive listener and understanding of INFPs emotions even if '
              'they are not understood. INFPs can benefit from ESTJs providing a more routine and structured life as '
              'foundation for order and effective action. Also be aware that ESTJs are not the strongest emotional '
              'communicators, so be sure to give them time to process their emotions to express them in their own '
              'way.',
        'p3': 'ESTJs can help INFPs expand their social circle and experience the world more; INFPs can provide ESTJs '
              'the courage to open up their mind to new possibilities for personal growth.'
    },
    'ESTJ x ISFP': {
        'p1': 'ESTJ-ISFP dynamic has the potential to complement each other through opposing Te/Fi, however this pair '
              'will need to be mature enough to find middle ground in emotional communication and understanding. ESTJs '
              'are often disconnected from their true feelings and emotions due to inferior Fi, while ISFPs are very '
              'much the opposite in being highly in tune with themselves and their personal needs based on their '
              'dominant Fi. This pair will need to work together to find openness and be vulnerable with each other to '
              'find a deeper level of connection.',
        'p2': 'ESTJs can work to become closer with their ISFP counterpart through respecting their need for personal '
              'time, exercising active listening and taking genuine interest in what they have to say by asking '
              'meaningful questions. ISFPs can strengthen their bond with ESTJs through striving to do what is said '
              'will be done and when it was said it would be completed. Look to frame your perspective, via '
              'suggestions or arguments, using logical reasoning rather than relying on emotional output.'
    },
    'ENTP x INFJ': {
        'p1': 'The ENTP-INFJ pair creates a rich and thoughtful companionship, one that will always question the '
              'boundaries of reality. The ENTP is a highly curious type that thrives off of questioning accepted '
              'norms, and exploring what could happen if things were changed or viewed differently. Meanwhile, the '
              'INFJ has a deep understanding for why things exist as they do, these observations can carve a path for '
              'the ENTP and can lead to a conversation for both parties to enjoy.',
        'p2': 'The ENTP can sometimes thrive on intellectual discussion that has no grounded purpose, which an INFJ '
              'needs. INFJs may feel dismayed by discussions or debates/arguments that have no goal in mind. The ENTP '
              'can also sometimes feel the need to argue on behalf of the side they disagree with in order to see the '
              'whole picture. This can come across as aggressive or again, pointless, to the INFJ that isn\'t prepared '
              'or aware of what\'s going on. ENTPs are also caring people, so their approach when helping someone '
              'often includes exploring and understanding all options before moving forward, which can be overwhelming '
              'to the INFJ.',
        'p3': 'INFJs\' insights are deeply rooted and understood to themself. But due to tertiary Ti, they may have a '
              'difficult time explaining their perspective satisfactorily to the ENTP. ENTPs\' aux-Ti thrives on '
              'understanding, and the INFJ may feel resisted against or unheard if they feel they can\'t properly '
              'express their view. An ENTP may ask a lot of questions to accelerate the process, but may actually '
              'overwhelm the INFJ. Patience is key for both types in order for this match to thrive and succeed.'
    },
    'ESTP x ESTP': {
        'p1': 'ESTP-ESTP pairing make for a very energetic and active couple. Sharing all four type preferences, they '
              'have common needs and goals. Both are likely to enjoy sports and outdoor activities. Both are '
              'spontaneous thrill seekers and will enjoy plotting their adventures together. Neither of the two '
              'partners tends to overcomplicate things, and the relationship feels just right.',
        'p2': 'Being in a relationship with someone of your own type means to share the same shortcomings as well. In '
              'this dynamic, neither will likely bother with mundane tasks, such as doing chores or paying bills. Both '
              'tend to act without thinking of consequences and neither will likely want to stick to a budget.',
        'p3': 'Even in same type relationships, there typically is a more responsible partner who is left to deal '
              'with all the unpleasantness alone. This may lead to resentment and disagreements, although ESTPs don\'t '
              'take things too seriously and likely will not allow minor issues ruin their relationships.'
    },
    'ESTP x INFJ': {
        'p1': 'The ESTP-INFJ pairing can be one considered ideal for self-growth. Sharing the same function stack '
              '(but inverted), both types are incredibly strong in the other\'s weakest points. So with time, '
              'experience with their partner will accelerate the journey to a more well-rounded and fully-realized '
              'self.',
        'p2': 'ESTPs have a reputation for being quite forward and blunt about their feelings and intentions. Their '
              'happy-go-lucky nature is accompanied by a very clear vision of what they want. ESTPs know exactly what '
              'that is, and arent afraid to go out and get it. These characteristics can drive the INFJ to do the '
              'same. The ESTP will encourage the INFJ to seek out what they want, instead of constantly pondering what '
              'will happen along with way. Action (or what they deem to be too much too fast) can be a pain-point for '
              'the INFJ, but the ESTP will work to lower those barriers and push the INFJ towards realizing the '
              'successes they dream of.',
        'p3': 'Meanwhile, the INFJ\'s contemplative and thoughtful nature will help bring the ESTP back down to earth '
              'in their own way. ESTPs can have an act now-think later approach, which the INFJ will often criticize.'
              'With time, the ESTP will be able to tolerate giving thought to the repercussions and consequences of '
              'success and failure. These insights will help the ESTP understand how to anticipate and combat the '
              'roadblocks that may be standing in their way.',
        'p4': 'The likelihood of success with this pairing rests almost entirely on how mature both types are, and '
              'how willing they are to accept differences and take criticism. Each type\'s pain-point is the other\'s '
              'preferred way to live, so both types must be willing to face their weaknesses in order to grow and '
              'prosper.'
    },
    'ENFP x ENFP': {
        'p1': 'The ENFP-ENFP duo is bound to be one filled with curiosity, depth, and new experiences. ENFPs together '
              'will likely be incredibly flexible in their adventures.',
        'p2': 'ENFPs together can encourage one another to push one their perception of the world, and will work to '
              'spark joy into each other\'s lives. ENFPs will also grow more and more aware of what works for their '
              'partner, and will tailor their ideas to accommodate those boundaries.',
        'p3': 'The area they will need to exercise a lot of caution over is with regards to each other\'s time, as '
              'well as when their boundaries conflict. It\'s pretty common for ENFPs to lose fulfillment in their '
              'relationships if their Fi isn\'t known and respected. In order for both members to keep the fire alive, '
              'it is important for them to communicate for one another regarding their current emotional state, '
              'especially if they are feeling exhausted or unfulfilled. And the other must be receptive of those '
              'emotions. Once one feels they can\'t be honest with the other, the relationship may deteriorate.'
    },
    'ENFP x ESFP': {
        'p1': 'There is a lot of overlap and shared interests between the ENFP and ESFP. Both are fueled by adventure '
              'and curiosity, and arent particularly fond of feeling anchored down. These types will likely share a '
              'common interest for "getting" out and making memories.',
        'p2': 'The key difference that may impact their dynamic is how they perceive the world around them. ENFPs are '
              'lead Ne, so they view the world more theoretically and abstractly, entertaining many different ideas '
              'and possibilities. ENFPs love to ponder what the future may hold. ESFPs are lead Se, to their '
              'perception is less about the future and more focused on the experience itself as it is unfolding in '
              'front of them.',
        'p3': 'Due to this key difference, it is very important that the ESFP grows accustomed to entertaining the '
              'theoretical more often (which may be a struggle due to inferior Ni). They should also respect when the '
              'ENFP feels they shouldn\'t do something. ENFPs will need to develop more of an appreciation for the '
              'experiences in front of them. This shouldn\'t be too much of a struggle, but could trigger their '
              'inferior Si if they begin to feel they\'ve made a bad decision. Both should be open to experiences, but '
              'with relative moderation.'
    },
    'ENFP x INTJ': {
        'p1': 'ENFPs and INTJs tend to have a strong dynamic that is held together by shared strengths and intriguing '
              'differences.',
        'p2': 'ENFPs are lead Ne, which oftentimes meshes very well with the INTJ\'s lead Ni. Lead Ne and Lead Ni can '
              'serve to bounce off of one another; the ENFP can think of a plethora of ideas and possibilities, to '
              'which the INTJ\'s Ni can take and develop. Both types have Te and Fi (though one prefers the other).'
              'This leads to a relative synergy, and there will likely be a shared outlook on the values between the '
              'partners.',
        'p3': 'Potential for struggle may come from those slightly different preferences. ENFPs have Fi second and Te '
              'third, so their values are a bit more personal. They also have a strong connection to their emotions.'
              'INTJs have Fi third, so while the emotional relationship to their values is still there, its more '
              'distant. They also have a much stronger eye for what works and most applicable (Te). In turn, they may '
              'find themselves trusting their personal devotions to a less degree than their ENFP partner. An ENFP\'s '
              'exuberance and enthusiasm may also be overwhelming.',
        'p4': 'In short, these types are known for their synergy and shared interests. There is an intimate balance '
              'that these two may find with each other if they can settle their slightly different perspectives. The '
              'INTJ should be respectful and appreciative of the ENFP\'s enthusiasm and emotionally-driven lifestyle.'
              'Meanwhile the ENFP should be careful not to push the INTJ too hard with regards to their emotions. The '
              'INTJ is a bit more internal and may not appreciate being asked to be overly vulnerable.'
    },
    'ENFP x INFJ': {
        'p1': 'The ENFP-INFJ pairing is commonly referenced due to their highly-complementary nature. Despite having '
              'distinct differences, this coupling has very high potential due to each ability to cover the other\'s '
              'blindspots. INFJs are deep and contemplative individuals with rich minds, which the ENFP will gain a '
              'lot of joy from exploring. ENFPs contain a plethora of ideas for the INFJ to consider, which helps feed '
              'their minds and expand their view of the world in a meaningful way.',
        'p2': 'This pairing is ideal when both types are open to compromise and balance. The INFJ should exercise '
              'care in properly communicating their boundaries. They can feel compelled to let things slide, which can '
              'worsen if left unaddressed. The INFJ should also try their best to continue showing genuine interest by '
              'asking the ENFP questions that give them a way to express themselves. An ENFP will likely feel unvalued '
              'if they feel they aren\'t allowed to express their ideas.',
        'p3': 'The ENFP\'s outgoing and curious nature could combat the INFJ\'s need for routine and comfort if left '
              'unchecked. The ENFP should be considerate when an INFJ decides to speak up, and should be careful not '
              'to make a routine of pushing hard boundaries. The INFJ tends to be quiet and passive, and being unable '
              'to properly finish a thought may cause them to close up.'
    },
    'ESFP x INFJ': {
        'p1': 'The ESFP-INFJ pairing can prove to be a rich and thoroughly deep relationship if well-balanced. ESFPs '
              'contain an enthusiasm for Se experiences and adventures that will allow the INFJ to withdraw from their '
              'minds and experience the world in all its glory. The INFJ can also help ground and focus the ESFP, '
              'helping them realize the benefits of a more focused lifestyle.',
        'p2': 'A major trait that the ESFP has that the INFJ will benefit from is an appreciation for activity. INFJs '
              'can have a habit of developing a routine and not wanting to deviate from it. The ESFP can help ease '
              'them into the escapism that the world could bring. ESFPs will also help INFJs expand their social '
              'circle.',
        'p3': 'INFJs possess valuable insights that ESFPs may find off-putting at first, but will eventually come to '
              'appreciate and perhaps even seek out. INFJs are people-oriented, and will assist the ESFP in sniffling '
              'out people and activities that may not be worth their time (if they can convince them of why). INFJs '
              'can also help the stressed ESFP expose mistakes that may be repeated, and help the ESFP develop a '
              'course of action to correct them.',
        'p4': 'This pairing can succeed as long as they can respect each other\'s prefer lifestyle. The Se-dominant '
              'ESFP doesn\'t like to feel caged in, and while the INFJ can help them develop a more orderly lifestyle, '
              'they still need to give the ESFP room to explore and live life. Likewise, the ESFP should work to '
              'appreciate the INFJ\'s need for regularity. An INFJ that is forced into unfamiliar situations will be '
              'overwhelming, and the INFJ will not enjoy feeling thrusted into new or ever-changing environments.'
    },
    'ISTJ x INFJ': {
        'p1': 'ISTJs and INFJs have the potential to be a compatible pairing due to their mutual desire for normalcy '
              'and control. Both type prefer to stick to their routine. However, how they arrive at that routine, or '
              'the reason why they follow them, could be a source of tension.',
        'p2': 'ISTJs like to adhere to what has worked for them before. Due to Si and Te, this type has a clear '
              'understanding for what has worked and what they may be comfortable trying. They also have a strong '
              'attention to detail. This can make them heavily by-the-book and practical people, with little desire to '
              'change something if it proves effective.',
        'p3': 'INFJs are very similar, however, their efforts are directed towards anticipating patterns and future '
              'changes. INFJs seek to be prepared for adversary in order to reduce frustration. They like to feel they '
              'won\'t be blindsided. This could cause tension with the ISTJ if the INFJ sees a risk for trouble. Also, '
              'the ISTJ may be resistant to change because their inferior Ne will conflict with the INFJ\'s lead Ni.',
        'p4': 'With that said, once the INFJ and the ISTJ come to an agreement on how things will be done and what to '
              'expect moving forward, these types will likely enjoy a calm and slow lifestyle that both may find '
              'fulfilling.'
    },
    'INTP x INFJ': {
        'p1': 'INTPs and INFJs share a lot of commonalities that can lead to an overlap in thought. The INTP craves '
              'intellectual conversations with their dominant Ti, and the INFJ can provide perspectives and '
              'well-developed ideas that can provoke a lot of thought in the INTP through their dominant Ni and '
              'tertiary Ti. Meanwhile, the INFJ benefits from learning how to better-balance their feelings with what '
              'they feel makes sense.',
        'p2': 'A probable source of friction between the types is their relationship to emotions. INFJs are deeply '
              'emotional people, despite their emotions not always boiling to the surface. More importantly, INFJs '
              'tend to be much more comfortable weighing other people\'s values and emotions. The INTP can consider '
              'others\' emotions and values as well, but due to inf-Fe, may have a hard time marrying them to their '
              'logical framework. The INTP will need to be capable of listening to an INFJ and may find themselves '
              'providing emotional support more than they would prefer.',
        'p3': 'Likewise, the INFJ should take the time to listen to the INTP when they present their logic. INTPs are '
              'problem solvers and helpers, and an INTP can feel incredibly shut out or unappreciated if an INFJ '
              'quickly dismisses their ideas.'
    },
    'ISTP x INFJ': {
        'p1': 'ISTPs and INFJs share all of the same functions, but their respective stacks are very different. And '
              'thus, their perspectives may see some overlap, but will still be very different.',
        'p2': 'ISTPs filter their perception of the world through what they feel makes sense, and they seek logical '
              'consistency in everything they do. ISTPs tend to be very practical people. They will help guide the '
              'INFJ and steer their intuition in the right direction, providing the Se-insights that the INFJ tends to '
              'overlook or even avoid. INFJs will need to be aware of this and work to communicate effectively and '
              'directly back to them. INFJs should also be aware of the ISTP\'s straightforward nature.',
        'p3': 'INFJs will likely help the ISTP develop emotional awareness while maintaining their precise '
              'communication skills. ISTPs tend to struggle with how to navigate the emotional values of others '
              'because it oftentimes conflicts with what they feel makes sense. The INFJ will help the ISTP put those '
              'conflicting perspectives together.',
        'p4': 'In short, the ISTP and INFJ are relatively balanced where their partner is not. If they can overcome '
              'the initial rift in perception and communication, these two can come together to create a very '
              'well-rounded and strong unity.'
    },
    'INFJ x INFJ': {
        'p1': 'The INFJ-INFJ partnership can be incredibly empowering. Not many other pairings will be able to '
              'replicate the dense level of understanding and appreciation for one another quite like this one.',
        'p2': 'Two INFJs together can generate a rich and cohesive world built for each other and by each other. Due '
              'to similar thought processes and similar quirks, this pairing is likely to have dense intimacy.',
        'p3': 'INFJs together should be aware of each other\'s compromising nature. They naturally seek out other\'s '
              'opinions before making a decision, which can slow the process down when neither INFJ has an opinion of '
              'their own. They are also liable to mirroring or adopting the other\'s emotions to a fault due to '
              'aux-Fe. They should be careful with how they handle themselves around one another during times of '
              'stress. One will almost certainly come to the aid for the other, but often at their own detriment.'
    },
    'INFJ x ISFJ': {
        'p1': 'Both INFJs and ISFJs have a reputation for being intensely caring and giving individuals, so this pair '
              'may offer a surprising amount of affection, emotional depth, and understanding.',
        'p2': 'These two types place high value on what they believe will benefit the other, and tirelessly chase '
              'after whatever will make their partner happy. They are keen on picking up what will accelerate that '
              'process, and will not be afraid to shower their partner with affection.',
        'p3': 'Potential areas of tension may arise when trying to understand how the other arrived at the conclusion '
              'they did. INFJ\'s Ni leads them to be innovative forward thinkers, and will try to solve problems '
              'before they arise. The ISFJ may have difficulty understanding why an INFJ is so certain of an outcome '
              'that hasn\'t happened yet. Meanwhile, the ISFJ tends to use their past Si experiences to organize a set '
              'of expectations, and their microscopic attention to detail may be overwhelming to the INFJ. Both types '
              'will likely have to take extra time to hear their partner out in order to arrive at a consensus.'
    },
    'INFJ x INFP': {
        'p1': 'Assuming both types allow the other into their inner worlds, the INFJ-INFP pairing has the potential '
              'to be an extremely fulfilling relationship.',
        'p2': 'The success of this pair rests mostly on values and boundaries. Both types must agree on what is '
              'acceptable and not acceptable. The INFP has strong core Fi values that need to be voiced, and the INFJ '
              'needs an expectation of how the relationship will be handled moving forward. Likewise, the INFJ should '
              'make it a routine to regularly communicate their feelings to the INFP. The INFP thrives off of clear '
              'communication, and the lack thereof may cause them to worry.',
        'p3': 'Both types need to respect each other\'s time alone. Despite the sparks and mutual intimacy that may '
              'come from this pairing, both types will need time to themselves to recharge. One type nagging the other '
              'could be seen as overbearing or overwhelming.'
    },
    'INFJ x ISFP': {
        'p1': 'ISFPs and INFJs may find themselves a handful of overlapping views and values. Both have an '
              'appreciation for beauty and harmony that they may seek to experience or create.',
        'p2': 'In order for this pairing to succeed INFJs need to realize that ISFPs need to have a clear conscience '
              'about what they are doing. INFJs should be careful to not push too hard against the ISFP if they '
              'disagree or do not understand their motivations. INFJs should also work to come out of their shell and '
              'engage in their partner\'s interests. ISFPs are quite practical and driven people. The INFJ may find '
              'some of these things superficial, but should work to approach these interests with an open and an open '
              'heart. Their ISFP may surprise them with something they will enjoy too.',
        'p3': 'ISFPs should be aware that INFJs have a keen awareness for patterns and what to expect. Their '
              'livelihood dwells on expectations in preparation for the future. This may cause the INFJ to suggest '
              'changes in action or criticize what\'s being done. ISFPs should resist taking these criticisms '
              'personally due to Fi, should understand that the INFJ isn\'t trying to be rude or insulting, but '
              'helping coerce their partner in a direction they feel will make them happy.',
        'p4': 'If both types can accomplish these things, the ISFP-INFJ relationship will be filled with an intensely '
              'loving and easy-going atmosphere. Their shared experiences and intimate connection can create a '
              'balanced and eventful relationship if kept in-check.'
    }
}


class MBTICore(object):
    mbti_list = mbti_list
    mbti_chart = mbti_chart
    mbti_overview = mbti_overview
    mbti_types = mbti_types
    mbti_functions = mbti_functions
    mbti_compatibility = mbti_compatibility
