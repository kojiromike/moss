# Managed Object Store by SmiTTY

In the README for this repo, please include the following:
- Why you chose to implement what you did
- Considerations, decisions, assumptions you made
- The next few improvements you’d make, and what challenges might exist

## Why I chose to implement what I did

While nothing in the work sample said it had to be a web application with a web API, I thought that direction would provide the most flexibility for future changes. Having decided on a web API, I decided to use Django because I know Python very well and, with django rest framework, it provides a way to create both an API and a GUI.

I sketched out the API, but didn't spend time working on a GUI, other than to enable the Django admin. This approach leaves us with several options for a GUI - we could implement a GUI in Django, or create a standalone application (web, mobile, or whatever).

I thought creating a reliable interaction with both the database and s3 would be the tricky part, so I wanted to tackle that first. I decided to keep it simple by only using a single bucket, and leaving the isolation up to the permissions model in the application.


## The Cloud

As a PoC, this is only designed to work with S3 for now. It could be extended to work with GCloud, etc, but would require some effort to do so. Authenticating to S3 uses boto3's default credential chain via a profile name, currently hard-coded to "moss".


## Configuration

As it says in src/moss/settings.py, it should be more 12-factor friendly, but hard-coding most settings was expedient for now.


## Testing

The basic tests are there, but the tests are incomplete. There's work to be done on permissions, so building out a lot of tests around permissions would be my next step.


## Setup and Demo Notes

- Run `poetry run ./src/manage.py createsupertenant` instead of the usual `createsuperuser` to avoid a constraint violation creating the user.
- Run `poetry run ./src/manage.py createusertoken $id | jq -r '"Authorization: Bearer \(.access)"' > token_{username}.txt` to create a file you can use for curl commands for a given user.


## Next Steps

### Structure and Testing

1. Now that the application has some useful behaviors testing should be a priority.
2. For expedience I mostly let django tooling determine the layout of the application. It'd be nice to structure the application more intentionally.
3. I could iterate faster with some useful fixtures to load for local development and testing.

### Authentication and Permissions

1. Currently we have to create permissions manually. Many permissions should be assigned automatically based on normal flows, such as:
  - The admin should automatically get permission to view and edit files.
  - Probably the file creator should be an admin on the file they create.
  - It may make sense for a user in a tenant to have some kind of access to all future files in that tenant.
  - A user should probably not be able to list all files in their tenant -- they should only be able to list files they can otherwise access.
2. Users will need a sensible way to get their JWT tokens. Right how that's manual.
3. It maybe should be an error to try to assign permissions across tenants. (Then again, this is worth some thought, as sharing across tenants isn't always a bad thing.)

### Implementation

1. Download doesn't actually download the file. It probably should. (Right now it prints out its presigned url.)
2. DRF has a nice feature for bulk handling. It might be nice to be able to upload or download multiple files at a time.

### Operations

1. The database should probably be PostgreSQL if we want to scale and take advantage of some of its features.
2. We should probably provide a Dockerfile or otherwise containerize the application.
3. There are opportunities to improve the local development setup, by standardizing on how certain things, such as tests are run.
4. I'd also probably build out CI using e.g. github actions.

## Challenges

Scaling: Using a single bucket and the tenant name being the only programmatic part of the prefix means that this thing can't scale as effectively as it probably should, and has the potential for a noisy-neighbor problem. This could be fixed by using more buckets or by introducing a uniformly distributed random hash to the object prefixes.

Permissions: It'd be a lot more secure and in the long run nicer to integrate permissions directly with IAM instead of using the django permissions model. However, it would require significant effort, and might not be worth it, especially if this thing should be multi-cloud.
