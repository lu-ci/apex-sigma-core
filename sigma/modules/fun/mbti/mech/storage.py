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

mbti_compatibility = {
    'estj': [2, 2, 2, 2, 4, 4, 5, 4, 3, 1, 3, 1, 3, 1, 3, 1],
    'esfj': [2, 2, 2, 2, 4, 4, 4, 5, 3, 1, 3, 1, 3, 1, 3, 1],
    'istj': [2, 2, 2, 2, 5, 4, 4, 4, 3, 1, 3, 1, 3, 1, 3, 1],
    'isfj': [2, 2, 2, 2, 4, 5, 4, 4, 3, 1, 3, 1, 3, 1, 3, 1],
    'estp': [4, 4, 5, 4, 2, 2, 2, 2, 1, 3, 1, 3, 1, 3, 1, 3],
    'esfp': [4, 4, 4, 5, 2, 2, 2, 2, 1, 3, 1, 3, 1, 3, 1, 3],
    'istp': [5, 4, 4, 4, 2, 2, 2, 2, 1, 3, 1, 3, 1, 3, 1, 3],
    'isfp': [4, 5, 4, 4, 2, 2, 2, 2, 1, 3, 1, 3, 1, 3, 1, 3],
    'entj': [3, 3, 3, 3, 1, 1, 1, 1, 2, 4, 2, 5, 2, 4, 2, 4],
    'entp': [1, 1, 1, 1, 3, 3, 3, 3, 4, 2, 5, 2, 4, 2, 4, 2],
    'intj': [3, 3, 3, 3, 1, 1, 1, 1, 2, 5, 2, 4, 2, 4, 2, 4],
    'intp': [1, 1, 1, 1, 3, 3, 3, 3, 5, 2, 4, 2, 4, 2, 4, 2],
    'enfj': [3, 3, 3, 3, 1, 1, 1, 1, 2, 4, 2, 4, 2, 4, 2, 5],
    'enfp': [1, 1, 1, 1, 3, 3, 3, 3, 4, 2, 4, 2, 4, 2, 5, 2],
    'infj': [3, 3, 3, 3, 1, 1, 1, 1, 2, 4, 2, 4, 2, 5, 2, 4],
    'infp': [1, 1, 1, 1, 3, 3, 3, 3, 4, 2, 4, 2, 5, 2, 4, 2],
}

mbti_overview = {
    'p1': 'Myers-Briggs Type Indicator (MBTI) is a self-report inventory analysis based on the work of Isabel Myers and mother Katherine Briggs, inspired by Carl Jung’s theory of personality types.',
    'p2': 'This self-report inventory takes into account one’s likes, dislikes, strengths, weaknesses, possible career preferences, as well as compatibility with other personality types. Such information provides insight into methods for self-actualization and personal development.',
    'p3': 'Each of the sixteen MBTI personality types are comprised of a combination of eight cognitive functions, originally developed by Jung. These eight functions are crucial to understanding how one interacts with both internal and external stimuli, and are beneficial to know as a tool to assist in further analysis and consideration of how one operates.'
}

mbti_types = {
    'enfj': {
        'stack': 'fe-ni-se-ti',
        'p1': 'The FeNi is an expert relationship builder. Through Fe they can sense and assess where someone else is at in life or a certain situation. This may allow them to share in part of a friend’s feelings as their friend describes a situation they feel particularly strongly about. The FeNi will feel true indignation, joy, anger, etc. on behalf of others, making them master empathizers. Those around the FeNi will typically describe them as warm, caring people, and great friends.',
        'p2': 'FeNi’s use their Ni to intuitively know what needs to be done before it may even become a real issue. They tend to exhibit a natural foresight, anticipating needs 10 steps before others do. come from a perspective of looking 10 steps ahead of others, and can see the need before others do. They might even feel that people don’t appreciate what they do because they do something before the need is actually there. They might also refrain from taking an action they know someone needs because they don’t want to seem presumptuous. Because FeNi’s enjoy helping people and get energy from meeting people’s needs, FeNi individuals should be careful to surround themselves with good-willed, honest people so as to not “give” themselves to death.',
        'p3': 'The FeNi spends a good deal of their internal thought life thinking about relational issues—how their actions affect others and how they feel about what others said to them. They often realize after the fact that something they said could have been taken in a way they did not intend, which can cause them to worry that they might have unintentionally hurt or offended someone. They spend a lot of time thinking about future possibilities like their goals and aspirations. They might not think about these things in a step-by step way. Rather, they want to explore different possibilities of where their goals and interests might lead them.'
    },
    'enfp': {
        'stack': 'ne-fi-te-si',
        'p1': 'NeFi’s are constantly chasing new shiny ideas and studying fresh topics of interest. They derive satisfaction from learning about a huge variety of topics so they can use the information to fuel their ideas. The more diverse their learning and exploring is, the more likely it is that they can find a unique solution to a problem by pulling from their library of knowledge or understanding.',
        'p2': 'NeFi’s are extremely self-aware and spend a good deal of time on self-reflection. They are very concerned with the depth and nuances of their values system and spend a large amount of their mental space clarifying, sifting, and refining their beliefs. This process can be very connected to deep emotions for NeFi’s. They might find themselves laughing or crying at the beauty of a seemingly random object that has meaning to them, while bystanders who notice their reaction might be quite confused at their sudden outburst. For some NeFi’s, their emotions run so deep that there have to have been a lot of feelings building under the surface for quite some time before they will burst forth. They tend to seek out things (movies, books, etc.) that will engage their emotions, because following characters they care about through an emotional journey can be very rewarding for them.',
        'p3': 'The NeFi’s instinct is to achieve inner harmony by remaining true to themselves, their own values, and minimizing the influence that external factors (societal expectations, and maybe even the opinions of friends and family) have on their values. They may love discussing their values with others, as long as they are able to remain true to themselves while doing so.',
        'p4': 'NeFi’s find their own principles to be trustworthy and valuable, and are inherently skeptical of  others that try to impose on them. If something does not line up with their beliefs, they cannot act in accordance with it. To go against their own values is to cause inner discord, which NeFi’s can’t tolerate for long.'
    },
    'entj': {
        'stack': 'te-ni-se-fi',
        'p1': 'TeNi’s are very goal-oriented and results-driven. When they’re at their best, you aren’t likely to see them continue with an inefficient method for long. They tend to dislike getting into the dirty details of implementation and are likely to delegate as much as possible to others. It’s very obvious to a TeNi what is or isn’t going to work, and it can be frustrating when others don’t see solutions as obviously as they do. TeNi’s may be accused of being bossy or critical at times, but it’s important to note that they typically won’t bother correcting someone unless they value that person and/or their work. Although people might complain about the bossiness of a TeNi, the truth is that those around them would be usually be lost without their effective leadership.',
        'p2': 'Although TeNi’s are very social people, they are not afraid of being disliked in most cases. They don’t shy from necessary confrontation and when it comes to interpersonal conflict, they are apt to want to resolve issues in a quick, efficient manner and then move on with life. Only when they feel someone has wronged them or wounded them very deeply will they feel the need to cut people out of their life. In most instances, they prefer to resolve an issue and move on, without lingering too much in any emotional aspects of conflict.',
        'p3': 'TeNi’s have a deep internal world that is often hard for them to put into words or share with others. Ni is their main source of creativity. They are very intuitive and can often see all the possibilities for how a particular situation will play out. They are then able to analyze all the options and refine them down until they arrive at what they feel is the most likely one. Their inner world is constantly shifting and changing and analyzing different aspects of things. When they make plans or have a goal in mind, they are naturally able to skip ten steps ahead to see how it might turn out.'
    },
    'entp': {
        'stack': 'ne-ti-fe-si',
        'p1': 'NeTi’s are constantly chasing new shiny ideas and studying fresh topics of interest. They derive satisfaction from learning about a huge variety of topics so they can use the information to fuel their ideas. The more diverse their learning is, the more likely it is that they can find a unique solution to a problem by pulling from their library of knowledge. They are commonly known as polymaths, or renaissance men/women because of the variety of topics they learn about. They generally prefer to obtain competence in many areas rather than mastering just one skill or area of expertise.',
        'p2': 'NeTi’s get their ideas from the world around them and their ideas usually flow best when they have someone to bounce ideas off of. This is the nature of Ne and other external functions (denoted by the lowercase “e”) - they need interaction with the world to function optimally. This is a double-edged sword, as the outside world can also be highly distracting. Because of this, they tend to need alternating stages of input and output.',
        'p3': 'NeTi’s tend to be curious about people, but having to constantly care for others can drain them quickly. They love studying people and brainstorming with them, but their default is often to try and problem-solve for people when they’re upset rather than only listening to them. It can take some direct instruction from others before the NeTi learns what is appropriate in terms of responding to others who are in emotional pain. They may also start to feel uncomfortable around overly emotional people, and can have a strong desire for the other person to just feel better so things can be normal again.',
        'p4': 'NeTi’s are constantly taking in information and turning it over in their minds, looking at it from every angle and thinking about how it relates to everything else they’ve learned. They regularly ask “how does this work?” and “why is it like this?”  as their Ti filters and processes their discoveries to separate out what is useful or not useful, accurate or not accurate.'
    },
    'esfj': {
        'stack': 'fe-si-ne-ti',
        'p1': 'FeSi uses Fe to “read” the vibes of everyone in the room and is constantly keeping tabs on what everyone seems to be thinking and feeling. They subconsciously take in all this information, and make most of their choices based on this info, which essentially boils down to, “What can I do that will benefit the most people?” At the same time, the FeSi also uses their own mannerisms, expressions, emotions, and capabilities to influence and help others around them. When the FeSi gets good vibes, feelings, or a sense of something that sparks their interest from another person or group of people, they build on that expression and mirror it back to the person or group.',
        'p2': 'FeSi’s tend to be especially intelligent when it comes to reading facial expressions and body language. When they scan the room, they subconsciously take in the “aura” or “feeling” that radiates from each individual person. In the mind of an FeSi, this process categorizes the “feeling” gleaned from each person and notes the person’s facial expression, gesticulations, body placement, etc. and stores them away to be accessed and pulled from later.',
        'p3': 'FeSi’s are very concrete inside—they have a sense internally that their world is very black and white; ‘right’, and ‘wrong’. Because of this, FeSi’s can be incredibly hard on themselves. They tend to set very high standards for themselves, because they believe that anything less is unacceptable. FeSi’s can use this to their advantage to create things with excellence, but they should be careful not to get so caught up in it that they don’t actually put anything out there because they feel it isn’t good enough, or become so focused on making things perfect that they lose sight of what actually matters.'
    },
    'esfp': {
        'stack': 'se-fi-te-ni',
        'p1': 'SeFi’s are all about in-the-moment, tangible, concrete, real world experiences and perceptions, and how they can connect their physical surroundings to their shifting, mystical inner world. It’s possible that those with strong Se are the only people who truly live ‘in the moment’, in a sense. They view the world as a solid force, and prefer to take in information in a concrete, solid way. Because they do not experience solidity within themselves, they seek that stability in the world around them.',
        'p2': 'SeFi’s especially feel that every moment should be spend on something worthwhile and fun, and doing anything they view as ‘work’ is arduous and tedious, even if it’s work they enjoy. They are all about having fun and experiencing new things, so even enjoyable work is rarely a favorite activity for them. They want to be able to do exactly what they want to do, the moment they think of doing it. Anything that hinders that freedom is a frustrating block to their Se.',
        'p3': 'While they can be great listeners, SeFi’s really enjoy doing things with people as a means of getting acquainted. They crave thrill and adventure and need to be engaged with the world around them. Exploring nature, getting involved in physical sports, or getting their hands dirty and doing things in the physical world is very cathartic for them.',
        'p4': 'At their best, SeFi’s are masters of self-care and great at putting healthy boundaries in place. They are empathetic people, so they see the needs of others and want to take care of them when they can. However, healthy SeFi’s know that they cannot effectively care for others unless they first care for themselves. They know their limits and aren’t usually afraid of saying ‘no’ when they aren’t able to do something or fit something into their lives.'
    },
    'estj': {
        'stack': 'te-si-ne-fi',
        'p1': 'TeSi’s are generally very organized people. This is not to say they’re all perfectly tidy, but when it comes to something that matters, they plan, organize, and execute their plans in a very linear fashion. When they put their all into a project and have the right tools and resources, you can be sure it will be very well executed.',
        'p2': 'TeSi’s are great at seeing areas for improvement in people’s lives. Because highly detailed systems naturally make sense to them, they may see a problem someone is having and try to help the person implement their own system as a solution. When they’re younger, they might try to apply their solutions to any potentially relevant problem they come across, thinking, “If it works for the me, of course it should work for the person I’m helping!” As they gain more experience in life, they learn to recognize when their help is welcome and where their solutions are actually a good fit, and they become a lot more strategic about the way they help people.',
        'p3': 'TeSi’s tend to have very high standards for themselves, which can cause them to focus on where they feel they’re falling short, even though those around them rarely demand the near-perfection they demand of themselves. Because they can be very driven and often end up in leadership roles where they’re the pioneer, it can get exhausting if they’re in a role where most of what they hear is negative feedback. Being a leader causes all their flaws to become more visible, and the perception most people have of TeSi’s is that they have no feelings at all. This can cause employees and even family members to be unnecessarily harsh in the way they speak to and about TeSi’s.'
    },
    'estp': {
        'stack': 'se-ti-fe-ni',
        'p1': 'SeTi’s have a strong need to be engaged in physical activity and DOING stuff in a tangible way, ideally being able to go as far as their physical limits allow and not having to interrupt the flow of the activity.',
        'p2': 'SeTi’s need a certain level of impulsiveness in life to be happy. While they don’t absolutely abhor schedules, it does get irritating for them when a schedule becomes more important than doing the things a schedule is supposed to allow time for. They also might break the rules from time to time, but not necessarily to rebel or make a point. They simply don’t think in terms of rules and procedures. Their focus is on actions that will accomplish specific things.',
        'p3': 'SeTi’s really enjoy doing things with people as a means of getting acquainted. They crave thrill and adventure. Exploring nature, getting involved in physical sports, or getting their hands dirty and doing things in the physical world is very cathartic for them. The Se side of an SeTi makes them value beauty very highly, and they are likely to seek out beautiful, serene surroundings, especially in nature. Their surroundings have a strong influence on them, and they are very aware of their physical environment.',
        'p4': 'SeTi’s are excited about the here and now of what is going on around them. They are very present, and might find it difficult to plan far into the future. They are so fully present in the moment that the current situation they find themselves in feels like it’s their whole world. If you were to ask an SeTi what their life is like, they may tell you about their current circumstances rather than the big picture.'
    },
    'infj': {
        'stack': 'ni-fe-ti-se',
        'p1': 'NiFe’s tend to have a rather large “working memory,” meaning that they can retain active consciousness of a large number of facts or details for immediate use. In the short term, they can have a remarkably accurate memory showing a great attention to detail, while still retaining the big picture. However, if they spend too much time trying to hold multiple perspectives and a wide array of details in their mind, they will suffer from internal overstimulation; this can even lead to moments of panic or feeling trapped inside of one’s head. It can also be a huge killer of the NiFe’s natural creativity.',
        'p2': 'The presence of Fe in an NiFe’s life is often experienced as a blessing and a curse. When they sense the emotions of other people, Ni’s vague, impressionistic nature often means that they don’t always clearly perceive origins and reasons for their emotional impressions. This is especially true for young NiFe’s who may not be able to clearly define why they dislike being around certain people or put in certain situations. It is the development of Ti  that allows them to retrace the steps that Ni traversed subconsciously.',
        'p3': 'They overwhelmingly feel that their inner world is vastly more fascinating and colourful than the world around them, and they struggle to convey anywhere near the level of detail, beauty, or simply the humor of what they’re experiencing in their mind in a way that does it justice. Too much time being forced to engage with the real world can get really exhausting for NiFe’s. Finding ways to minimize this drain is a good way to allow them to focus their creative abilities on the things they are best at.'
    },
    'infp': {
        'stack': 'fi-ne-si-te',
        'p1': 'FiNe’s are masters of self-care and typically great at putting healthy boundaries in place. They are very empathetic people, so they see the needs of others and want to care for them. However, healthy FiNe’s know that they cannot effectively care for others unless they first care for themselves. They know their limits and aren’t usually afraid of saying ‘no’ when they aren’t able to do something or fit something into their lives.',
        'p2': 'FiNe’s are extremely self-aware and spend a lot of time on self-reflection. They are very concerned with the depth and nuances of their values system and spend a large amount of their mental space clarifying, sifting, and refining their beliefs. This process can be very connected to deep emotions for FiNe’s.',
        'p3': 'For some FiNe’s, their emotions run so deep that there have to have been a lot of feelings building under the surface for quite some time before they will burst forth. They tend to seek out things (movies, books, etc.) that will engage their emotions, because following characters they care about through an emotional journey can be very rewarding.',
        'p4': 'The FiNe’s driving instinct is to achieve inner harmony by remaining true to themselves, their own values, and minimizing the influence that external factors (societal expectations, and maybe even the opinions of friends and family) have on their values. After a lengthy discussion, FiNe’s need time by themselves to evaluate the conversation and consider what the other person said and how they might fit it into their value system.',
        'p5': 'FiNe’s have a world of theories that are swirling around at any given time, and it’s important for them to have time alone in order to develop them. Their best ideas will usually come when they have a sense of inner peace and enough inspiration. Many FiNe’s find mindfulness, meditation, or another form of intentional relaxation to be useful for obtaining peace.'
    },
    'intj': {
        'stack': 'ni-te-fi-se',
        'p1': 'NiTe’s have a very deep internal world. They are extremely intuitive and can often see all the possibilities for how a particular situation will play out. They are then able to analyze all the options and refine them down until they arrive at what they feel is the most likely one. They may even be able to use this to predict the future in a sense.',
        'p2': 'NiTe’s really like improving things. They tend to enjoy work where they get to combine their ability to see ten steps ahead with their drive to make things better and more efficient. Some examples could be engineering, product design, architecture, or the sciences. They also tend to be interested in solving big practical issues like pollution or overpopulation.',
        'p3': 'NiTe’s tend to be very deliberate about the choices they make and they like to do things with excellence when they’re working on something they care about. This means that doing the right work, they are extremely responsible and determined. With the wrong work, they may get irritable and apathetic about the way the job is done, or may focus too much on little details without being able to see what’s most important in the context of the big picture. It’s important that they gain the self-awareness needed to know the difference.',
        'p4': 'NiTe’s internal world has a certain intensity to it that they may feel is lost once it’s brought out through verbal communication. They tend to be more at ease communicating through images, sound, written word, or some other form of expression where they are able to explore the full depth of an idea and expand on it before presenting it to public scrutiny. They are also usually more interested in finding the meaning behind things than taking them at face value, which means they may take some time to process new opportunities or unusual circumstances they find themselves in.'
    },
    'intp': {
        'stack': 'ti-ne-si-fe',
        'p1': 'Ti is primarily concerned with learning. Not just gaining knowledge, but understanding complex things in a deep way. TiNe’s see the possibilities available using Ne, pick things apart into their smallest components so that each detail can be stored using Si, and then apply this information across a variety of situations using Ne.',
        'p2': 'TiNe\'s need to withdraw from the world often in order to process all of their observations. They often spend a significant amount of time searching for cognitive biases within themselves so they can remove them and therefore be more objective in their analyses.',
        'p3': 'TiNe’s have a world of theories that are swirling around at any given time, and it’s important for them to have time alone in order to develop them. Their best ideas will usually come when they have a sense of inner peace and enough input. Many TiNe’s find mindfulness, meditation, or another form of intentional relaxation to be useful for obtaining peace. As far as input goes, learning interestings things or having an intellectual conversation with someone are safe bets.',
        'p4': 'For the ideas that have had some time to percolate, the TiNe needs to have places for output. Whether it’s writing, speaking, teaching, building, designing, or something else, it’s important to have space to string together the things they’ve studied in a unique way. This can also help them to refine and perfect the expression of their ideas. While they may feel like they understand something fully in their head, and they often make great teachers, they may not be as adept at explaining things to others without previous practice.'
    },
    'isfj': {
        'stack': 'si-fe-ti-ne',
        'p1': 'Si is internal or introverted Sensing. It’s all about real-world experiences, and how 5-senses (seeing, hearing, tasting, seeing, smelling) affect people with Si. SiFe’s value their own experiences very highly, and typically have a very good memory or catalogue of details about them.',
        'p2': 'SiFe’s are generally pretty in touch with the world around them because of their high value for real-world, tangible experiences. They tend to take care of life’s daily needs very well through an organized schedule or a to-do list planned out in their heads. Because the to-do list in their head is being added to just as quickly as they check things off, they may feel that they haven’t accomplished much unless they are able to see tangible results from their efforts.',
        'p3': 'SiFe’s are very reliable and dependable, and they expect the same from others. It can be frustrating for them when they can understand and see the steps needed to complete a project, but others around them can’t seem to see the work and details that will be necessary - especially when it’s the people who they need help from in order to accomplish their goal.',
        'p4': 'SiFe’s also tend to have very high standards for themselves, which can cause them to focus on where they feel they’re falling short, even though those around them probably don’t demand the near-perfection they demand of themselves.',
        'p5': 'SiFe’s strong internal sense of right and wrong can color their sense of themselves, as they naturally see all the things they aren’t perfect at (because their mental to-do list is never complete), and all the steps needed to obtain perfection, which overwhelms them. Because SiFe’s can naturally focus on what still needs to be done, using Fe feedback from other people to understand what they are really like in the world is a valuable process that can help the SiFe see the areas they are already excelling in.'
    },
    'isfp': {
        'stack': 'fi-se-ni-te',
        'p1': 'At their best, FiSe’s are great at knowing themselves, as they spend a lot of time on self-reflection. They are very concerned with the depth and nuances of their values; they spend a large amount of their mental space clarifying, sifting, and refining their beliefs. This process can be very connected to deep emotions, and they might find themselves laughing or crying at the beauty of a seemingly random object that has meaning to them, while bystanders who notice their reaction might be quite confused at their sudden outburst.',
        'p2': 'FiSe’s tend to have an active imagination well into adulthood. Fi dominant types are very concerned with The Story of/behind various things. For example, they might see a large, sturdy tree and wonder how long it’s been there, trying to imagine the events it’s been around for, or who else sat in its shade, what wisdom might be attached to or inside of that tree, etc. They automatically look for meaning everywhere—in books, movies, a passing remark from a friend, a special cup they like to use, or even why that tree was planted in a particular place.',
        'p3': 'FiSe’s tend to be very earthy, and are drawn to the mysterious, intuitive aspects of the world around them because of their Ni. They are all about in-the-moment, tangible, concrete, real world experiences and perceptions, and how they can connect their physical surroundings to their shifting, mystical inner world.',
        'p4': 'FiSe’s are typically very creative. Se likes very tangible, 5-senses (sight, touch, taste, smell, sound) experiences, so creating art with their hands (i.e. playing an instrument, painting, drawing, sculpting, photography, etc.) is very gratifying to them. In creating tangible art, they get to put Fi and Se to use by expressing meaning in all kinds of real-world ways that other people can experience.'
    },
    'istj': {
        'stack': 'si-te-fi-ne',
        'p1': 'SiTe’s are a practical, strategic thinkers that love pulling the best out of people and projects. Whatever they decide to do, it will probably involve maximizing potential.',
        'p2': 'Si is all about real-world experiences. SiTe’s, often without noticing, pay a lot of attention to how things that engage their 5 senses (seeing, hearing, tasting, seeing, smelling) affect them. They value their own experiences very highly, and typically have a very good memory or catalogue of details about them. They tend to store their impressions of experiences rather than direct memories of the experiences themselves. They use this information to help them make the best decisions possible in the future.',
        'p3': 'Despite some popular stereotypes, SiTe’s do change their minds, though it might take longer for them than for other types. They often have a quirky sarcastic sense of humour and care deeply for those close to them, though they are far more likely to show their love in practical ways rather than being sappy and overly affectionate.',
        'p4': 'SiTe’s manage concrete practical information more easily than abstract concepts. Because they are linear thinkers, they naturally ask themselves “What is the next step?”, and because they are detail-oriented, they are often able to manage or design highly complex systems and highly detailed projects with incredible grace.',
        'p5': 'SiTe’s tend to have very high internal standards for themselves, which can cause them to focus on where they feel they’re falling short, even though those around them probably don’t demand the near-perfection they demand of themselves. At times they may even get fixated on doing things “right” according to the rules they’ve internalized about how the world works, and in their younger years it’s not uncommon for them to try to impose these rules on their kids or people they’re trying to help.'
    },
    'istp': {
        'stack': 'ti-se-ni-fe',
        'p1': 'TiSe’s like to focus on real world problems and often have a strong appreciation for mastery and doing things with excellence and beauty. They don’t just want to learn, they want to be able to do something with it. Although they like having time to think about things, having Se means they can bypass Ti and take physical action when it’s clear and needed in the moment.',
        'p2': 'TiSe’s often have a thrill-seeking side, and may enjoy sports, gambling, skydiving, bungee jumping, adventure travel or speeding down the highway in a sports car or on their motorcycle. TiSe’s are often perceived based on this side of them that loves adventure and needs thrilling new experiences, but what people often don’t see is the sharp mind behind it all.',
        'p3': 'TiSe’s are often willing to jump out on a limb and task risks where many others are not. With their Ti performing an analysis of the situation and their Ni predicting how things will play out in the future, they can take leaps with a degree of certainty and thrill that others simply don’t have.',
        'p4': '	TiSe’s love achieving mastery. They want to feel like they can produce something excellent time after time. When they experience something that’s been done with beauty and excellence, their Ni gives them hints at why it’s beautiful and what makes it well-crafted.',
        'p5': 'TiSe’s like for people to get to the point and say what they really mean. They might get irritated when they feel like they are expected to pay attention and do all the right things in social situations.',
        'p6': 'Their lack of interest in adhering to social norms and love of logic should not be interpreted to mean that they do not care about other people in their lives. They simply show that they care in a straightforward, problem-solving way. Many TiSe’s do care deeply about social issues and the welfare of their communities, they just don’t usually have the emotional stamina to be “touchy feely” with more than a handful of people who are close to them.'
    }
}

mbti_functions = {
    'fe': {
        'name': 'Extraverted Feeling',
        'p1': 'The process of extraverted Feeling often involves a desire to connect with (or disconnect from) others and is often evidenced by expressions of warmth (or displeasure) and self-disclosure.',
        'p2': 'The "social graces," such as being polite, being nice, being friendly, being considerate, and being appropriate, often revolve around the process of extraverted Feeling. Keeping in touch, laughing at jokes when others laugh, and trying to get people to act kindly to each other also involve extraverted Feeling.',
        'p3': 'Using this process, we respond according to expressed or even unexpressed wants and needs of others. We may ask people what they want or need or self-disclose to prompt them to talk more about themselves. This often sparks conversation and lets us know more about them so we can better adjust our behavior to them.',
        'p4': 'Often with this process, we feel pulled to be responsible and take care of others\' feelings, sometimes to the point of not separating our feelings from theirs. We may recognize and adhere to shared values, feelings, and social norms to get along.'
    },
    'fi': {
        'name': 'Introverted Feeling',
        'p1': 'It is often hard to assign words to the values used to make introverted Feeling judgments since they are often associated with images, feeling tones, and gut reactions more than words.',
        'p2': 'As a cognitive process, it often serves as a filter for information that matches what is valued, wanted, or worth believing in. There can be a continual weighing of the situational worth or importance of everything and a patient balancing of the core issues of peace and conflict in life\'s situations.',
        'p3': 'We engage in the process of introverted Feeling when a value is compromised and we think, "Sometimes, some things just have to be said." On the other hand, most of the time this process works "in private" and is expressed through actions.',
        'p4': 'It helps us know when people are being fake or insincere or if they are basically good. It is like having an internal sense of the "essence" of a person or a project and reading fine distinctions among feeling tones.'
    },
    'ne': {
        'name': 'Extraverted Intuition',
        'p1': 'Extraverted iNtuiting involves noticing hidden meanings and interpreting them, often entertaining a wealth of possible interpretations from just one idea or interpreting what someone\'s behavior really means. It also involves seeing things "as if," with various possible representations of reality.',
        'p2': 'Using this process, we can juggle many different ideas, thoughts, beliefs, and meanings in our mind at once with the possibility that they are all true. This is like weaving themes and threads together.',
        'p3': 'We don\'t know the weave until a thought thread appears or is drawn out in the interaction of thoughts, often brought in from other contexts. Thus a strategy or concept often emerges from the here-and-now interactions, not appearing as a whole beforehand.',
        'p4': 'Using this process we can really appreciate brainstorming and trust what emerges, enjoying imaginative play with scenarios and combining possibilities, using a kind of cross-contextual thinking.',
        'p5': 'Extraverted iNtuiting also can involve catalyzing people and extemporaneously shaping situations, spreading an atmosphere of change through emergent leadership.'
    },
    'ni': {
        'name': 'Introverted Intuition',
        'p1': 'Introverted iNtuiting involves synthesizing the seemingly paradoxical or contradictory, which takes understanding to a new level. Using this process, we can have moments when completely new, unimagined realizations come to us.',
        'p2': 'A disengagement from interactions in the room occurs, followed by a sudden "Aha!" or "That\'s it!" The sense of the future and the realizations that come from introverted iNtuiting have a sureness and an imperative quality that seem to demand action and help us stay focused on fulfilling our vision or dream of how things will be in the future. Using this process, we might rely on a focal device or symbolic action to predict, enlighten, or transform.',
        'p3': 'We could find ourselves laying out how the future will unfold based on unseen trends and telling signs.This process can involve working out complex concepts or systems of thinking or conceiving of symbolic or novel ways to understand things that are universal. It can lead to creating transcendent experiences or solutions.'
    },
    'se': {
        'name': 'Extraverted Sensing',
        'p1': 'Extraverted Sensing occurs when we become aware of what is in the physical world in rich detail. We may be drawn to act on what we experience to get an immediate result.',
        'p2': 'We notice relevant facts and occurrences in a sea of data and experiences, learning all the facts we can about the immediate context or area of focus and what goes on in that context. An active seeking of more and more input to get the whole picture may occur until all sources of input have been exhausted or something else captures our attention.',
        'p3': 'Extraverted Sensing is operating when we freely follow exciting physical impulses or instincts as they come up and enjoy the thrill of action in the present moment. A oneness with the physical world and a total absorption may exist as we move, touch, and sense what is around us.',
        'p4': 'The process involves instantly reading cues to see how far we can go in a situation and still get the impact we want or respond to the situation with presence.'
    },
    'si': {
        'name': 'Introverted Sensing',
        'p1': 'Introverted Sensing often involves storing data and information, then comparing and contrasting the current situation with similar ones.',
        'p2': 'The immediate experience or words are instantly linked with the prior experiences, and we register a similarity or a difference—for example, noticing that some food doesn\'t taste the same or is saltier than it usually is.',
        'p3': 'Introverted Sensing is also operating when we see someone who reminds us of someone else. Sometimes a feeling associated with the recalled image comes into our awareness along with the information itself. Then the image can be so strong, our body responds as if reliving the experience. The process also involves reviewing the past to draw on the lessons of history, hindsight, and experience.',
        'p4': 'With introverted Sensing, there is often great attention to detail and getting a clear picture of goals and objectives and what is to happen. There can be a oneness with ageless customs that help sustain civilization and culture and protect what is known and long-lasting, even while what is reliable changes.'
    },
    'te': {
        'name': 'Extraverted Thinking',
        'p1': 'Contingency planning, scheduling, and quantifying utilize the process of extraverted Thinking.',
        'p2': 'Extraverted Thinking helps us organize our environment and ideas through charts, tables, graphs, flow charts, outlines, and so on. At its most sophisticated, this process is about organizing and monitoring people and things to work efficiently and productively.',
        'p3': 'Empirical thinking is at the core of extraverted Thinking when we challenge someone\'s ideas based on the logic of the facts in front of us or lay out reasonable explanations for decisions or conclusions made, often trying to establish order in someone else\'s thought process.',
        'p4': 'In written or verbal communication, extraverted Thinking helps us easily follow someone else\'s logic, sequence, or organization. It also helps us notice when something is missing, like when someone says he or she is going to talk about four topics and talks about only three.',
        'p5': 'In general, it allows us to compartmentalize many aspects of our lives so we can do what is necessary to accomplish our objectives.'
    },
    'ti': {
        'name': 'Introverted Thinking',
        'p1': 'Introverted Thinking often involves finding just the right word to clearly express an idea concisely, crisply, and to the point.',
        'p2': 'Using introverted thinking is like having an internal sense of the essential qualities of something, noticing the fine distinctions that make it what it is and then naming it. It also involves an internal reasoning process of deriving subcategories of classes and sub-principles of general principles. These can then be used in problem solving, analysis, and refining of a product or an idea.',
        'p3': 'This process is evidenced in behaviors like taking things or ideas apart to figure out how they work. The analysis involves looking at different sides of an issue and seeing where there is inconsistency. In so doing, we search for a "leverage point" that will fix problems with the least amount of effort or damage to the system.',
        'p4': 'We engage in this process when we notice logical inconsistencies between statements and frameworks, using a model to evaluate the likely accuracy of what\'s observed.'
    }
}
