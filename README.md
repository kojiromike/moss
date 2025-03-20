# Managed Object Store by SmiTTY

In the README for this repo, please include the following:
- Why you chose to implement what you did
- Considerations, decisions, assumptions you made
- The next few improvements you’d make, and what challenges might exist

## Why I chose to implement what I did

While nothing in the work sample said it had to be a web application with a web API, I thought that direction would provide the most flexibility for future changes. Having decided on a web API, I decided to use Django because, with django rest framework, it provides a way to create both an API and a GUI.

I sketched out the API, but didn't spend time working on a GUI, other than to enable the Django admin. This approach leaves us with several options for a GUI - we could implement a GUI in Django, or create a standalone application (web, mobile, or whatever).

I thought creating a reliable interaction with both the database and s3 would be the tricky part, so I wanted to tackle that first. I decided to keep it simple by only using a single bucket, and leaving the isolation up to the permissions model in the application.


## The Cloud

As a PoC, this is only designed to work with S3 for now. It could be extended to work with GCloud, etc, but would require some effort to do so. Authenticating to S3 uses boto3's default credential chain via a profile name, currently hard-coded to "moss".


## Configuration

As it says in src/moss/settings.py, it should be more 12-factor friendly, but hard-coding most settings was expedient for now.


## Testing

The testing framework is there, but the tests are incomplete. Mocking S3 calls requires some special effort and I decided to focus on the implementation.


## Setup and Demo Notes

- Need to run 'createsupertenant' instead of the usual django-admin 'createsuperuser' to avoid a constraint violation creating the user.


## Next Steps

### Permissions
1. Currently we have to create permissions manually. Many permissions should be assigned automatically based on normal flows, such as:
  - The admin should automatically get permission to view and edit files.
  - Probably the file creator should be an admin on the file they create.
  - It may make sense for a user in a tenant to have some kind of access to all future files in that tenant.
2. It should probably be an error to try to assign permissions across tenants.

### Implementation

1. Download doesn't actually download the file. It probably should. (Right now it prints out its presigned url.)

## Challenges

Scaling: Using a single bucket and the tenant name being the only programmatic part of the prefix means that this thing can't scale as effectively as it probably should, and has the potential for a noisy-neighbor problem. This could be fixed by using more buckets or by introducing a uniformly distributed random hash to the object prefixes.

Permissions: It'd be a lot more secure and in the long run nicer to integrate permissions directly with IAM instead of using the django permissions model. However, it would require significant effort, and might not be worth it, especially if this thing should be multi-cloud.
