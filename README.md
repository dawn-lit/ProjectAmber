# Project Amber

### Why I created Project Amber:

If you've known me for some time, you're aware of my avid enthusiasm for established on-demand cloud computing platforms like AWS. These platforms not only simplify the hosting of online services but also relieve individuals of concerns related to intricate aspects like DNS and web security. Nevertheless, owing to escalating costs and heightened security considerations, I've concluded that I must now take on the responsibility of maintaining my own infrastructure.



### The overview:

Currently, the infrastructure is tailored to support three of my critical web services: a [self-hosted GitLab](https://gitlab.dawnlit.com), a [code-server](https://github.com/coder/code-server) service, and [Dawn Lit](https://dawnlit.com/). Each component is meticulously segregated and encapsulated within individual Docker containers, streamlining the deployment process.

![overview](/assets/overview.png)

The infrastructure is presently configured and validated for operation on Ubuntu Server 22.04, with a future plan to migrate to 24.04 later this year. Additionally, there is flexibility for running the entire infrastructure on Ubuntu Desktop if that aligns with your preferences.



### How to deploy an infrastructure like this on your own server?

1. Configure the **configuration.json**.
2. On your server, run `sudo python3 setup_env.py` to set up the environment.
3. Run `sudo python3 setup_danwlit.py` to set up the infrastructure .

That is it.