\title{Apex Sigma 5.0}
\date{\today}
\author{Lucia's Cipher - Aleksa Radović}
\maketitle
\pagebreak

# Introduction

## Origin

**Apex Sigma**, commonly called **Sigma**, was started on **August 16th 2016**.
The project was supposed to be a Discord Bot that, aside from standard utilities,
had a connection to as many external APIs as possible. This idea was what gave Sigma
the title of *The Database Giant*. The project started with 50 APIs to consume,
some fell off and new ones got added as those that fell off either didn't have public
access points or simply had no API at all. Somewhere down the road this initial goal
got lost and abandoned. We instead started focusing on 3 things: community interaction,
utilities, and mini games. Now, this can't be called a bad thing in any sense, we want
to provide users with fun ways to interact, to help them do stuff easily, and give them
something to kill time with or compete against other users for.

## Current State

The current Sigma is doing great, at the moment when this is written, Sigma has **435**
commands and **62** event-triggered functions. Each second an average of **960** functions
are processed in the execution queues. The population is **~600.000** members and
**~12.000** guilds. That's awesome! And it's also a problem.
With the current infrastructure, Sigma is unable to function at an ideal level to
serve all those functions and users. Being written in **Python**, the project lacks
the desperately needed multiprocessing compatibility. One main worker thread can't handle
all of this load. And so we're here...

\pagebreak

# Design

## Structure

Referring to the general architectural structure of the entire software ecosystem.
The structure should be unbound but interconnected. To explain, it means that pieces of
the project can be placed on different machines, shards,
environments and still perform as one giant node-based unit.
This is the cause for the **Taskmaster** and **Handler** system.

## Task Distribution

So I said *"node-based"*, this mean two things: one is what was said above,
being able to have pieces in various locations and environments that are connected,
and it means it needs to have a *fire and forget* event driven system.
For example, a core of sorts sends a signal with the necessary data for a worker
to execute, but does not wait for the execution of that task or the workers response.
Aside from the response that the worker received the task.
Instead it moves on to other tasks that need worker distribution.

## Abstract

Nearly everything, if not everything, should be abstract and ready to be extended
or re-purposed at any time. Core components should be abstract enough for
new additions and new technologies to have an easy method of implementation.

## Environments

The original idea is having specific parts of the project in their own Docker container.

But let's go broader, let's give it the ability to, aside from launching new containers,

also be able to either launch new processes in the host environment, and launch fresh VPS
instances on specified and configured hosting services to handle these tasks.

\pagebreak

# Taskmaster

## Basic

The **Taskmaster** instance is a core that handles connecting to the select service of
choice and creates **Handlers** to take on the tasks given. This core both communicates
with the connected service and the handlers, taking appropriate action.

## Communication

Communication between the Taskmaster and Handlers should be done over methods without
direct or locking links. UNIX sockets, UDP ports, etc. based on preferences.
With the abstract nature of this project this shouldn't ultimately be an issue and
would result in a lot of supported environments.

## Events

The connected service should be handled in the form of events.
When the service transmits its own, the core sends an announcement signal that is then
handled by modules appended to the core.

## Modularity

The Taskmaster should be able to have new modules and plugins added to it.
Modules that read the above events and handled them appropriately.
Such as any changes in the core itself, signals from Handlers, and similar.

## Storage

The Taskmaster core should be the primary source of information for the Handlers.
Handling most of Database connections and Caching, as well as statistical details.

\pagebreak

# Database

Most databases have function other than simply storing and retrieving data.
Aside from basic CRUD functionality, there are offsets, limits, counters, bulk
instruction execution operation and many more.
Let's start with the basics, the database CRUD operations,
or the **C**reate, **R**ead, **U**pdate and **D**elete operations.
Each of them should have a bulk or multi-entry function and a single-entry alternative.
For example, MongoDB's `find()` and `findOne()`, and `delete()` and `deleteOne()`.
Mandatory indexing for all tables and collections in the database.

## Create

Stores new data in the database, nothing exotic, assuming the same data with the given
identifier doesn't exist and that it abides by other database limitations.
Such as periods not being allowed in MongoDB's keys as they indicate nested data.
If the given identifier exists, it should act like an **Update** operation.

## Read

Or **find** operations. Look up and find the queried data from the database.
Return the data within the given `offset: int` and `limit: int`.
Or alternatively if a single entry version is used, return the first single entry
that the database finds with the given criteria.

## Update

Updates existing documents, if the document doesn't exist, it acts as the **Create**
operation and creates the document instead. It should consist of at least the lookup
identifier argument, which document to update exactly, and an alteration argument,
being the data that needs to be changes by its given `key: value` pairs.

## Delete

Fully and permanently deletes a document or set of documents that fit the given
lookup identifiers or criteria.

\pagebreak

## Other Operations

Utility database function such as counting the number of documents in a search criteria
can be additionally added. In most cases they are supported natively but if they
are not, the CRUD can be used to mimic such a behavior.

## Flexibility

Most documents don't have static structures nor tables. They constantly change, new entry
fields are constantly added depending on new modules, mechanics, data, etc.
Not all databases support this, there needs to be a method to handle such a behavior.
Going the cheapest (performance-wise) route, we'll go with static schemas,
and make a *Schema Registration System*. This system will be a part of the
module loading mechanics and essential workflow.

## Operation Queue

Database functions shouldn't be executed immediately. They should have a constant
cache-like system in place where their respective operations are cached and queued.
You can imagine it like an in-memory pseudo database when it comes to retrieving
partly updated or newly created data. Once the queue clockwork picks it up, it's
stored in the database and the cache entry is removed.

\pagebreak

# Caching

It's not really a complex topic.
We should be able to `get()` a value, `set()` a value, and `del()` a value.
With abstraction along the way to make multiple types of caches. Such as
a base null cache, that just plain doesn't cache anything at all, memory and ttl caches,
and cache server services, such as Redis. Essentially a dictionary with extra steps.

## Data Types

The cache should be able to cache both primitive and complex data. Integers, strings, floats, arrays, dictionaries, objects, structures, everything.
Which assumes some sort of general serialization for given data to be stored.

## Limitations

*For memory cache types*.

The cache should have a maximum size it can reach that can be controled by a
configuration parameter. Syntax like `1024M` or `2G`, and the like.
This should be checked before adding an item in the cache.
If the sum of the new item's size and the current size of the cache are above the limit
pop the first entry in the cache. Getting rid of older entries and adding newer ones.
A heap-like method of storage.

## Overhead

If the cache is centralized in the Taskamster it'll cause overhead.
The goal of this is to reduce I/O and strain on the database.
Having it centralized in the Taskmaster might result in that load just
being transfered to the Taskmaster instead of the database.
Look into it being a `signal` updater instead.

## Signals

In the event that the caches are stored in each shard Handler itself,
and not stored in the Taskmaster and shared across shards,
there needs to be a way to notify the other handlers, and Taskmaster,
that a cache entry under a specific key is no longer valid and should be
refreshed. The caches need to be up to date with one another.

\pagebreak

# Configuration

## Reading

The congiration core should be able to pull data out of various types of storages.
Mostly referring to static plain-text file formats such as YAML, JSON or even XML.
But it should also be able to pull configuration parameters from the environment.
The safest(?) way to do this if we were to use all possible formats in a priority
hierarchy. For example, it should try to get the config value from the environment
variables, if it fails check for YAML files, then for JSON, and then for XML.
If nothing set is found, default to a hardcoded default value for the entry.
The configuration of the Handlers should be independent from the Taskmaster
but should use the Taskmaster's configuration value if none is set for the
handler itself. Meaning that the above sequence for checking for configurations
would include asking the Taskmaster for a configuration value in the end as well.

## Nesting

The configuration, in the end-total should be contained within one directory,
if specifically looking at file-based configuration.
Underscore connected values for the environment variable alternative.
Screaming snake case styled please.

The folder location should be something like:

> Files: `{root}/{core_type}/{component_type}/{component_name}`
>
> File Example: `./config/taskmaster/core/database.yml`

> Environment: `SIGMA_{core_type}_{component_type}_{component_name}`
>
> Environment Example: `SIGMA_HANDLER_MODULES_CAT`

To explain what each of those is:

- **root**: The root of the configuration folder, such as `/srv/sigma/config`.
- **core_type**: Possible values are `taskmaster` and `handler`.
- **component_type**: This referrs to it storying files for the `core` or `modules`.
- **component_name**: For the core, things like `database`, `cache`, etc. And for the modules file entries, the funcion name of the function it's bound to such as `cat` or `suggest`.

\pagebreak
