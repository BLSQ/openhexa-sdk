⚠️ This is the code for a previous, deprecated version of our pipelines engine.

Please use https://github.com/BLSQ/openhexa-sdk-python.

# OpenHexa SDK

- Interact with OpenHexa backend from notebooks and pipelines
- Feedback logs, messages, files for better frontend integration

**This is a beta, interfaces might change**

### Usage

In a pipelines, import the SDK & get your DagRun context:

```
import openhexa
dagRun = openhexa.get_current_dagrun()
```

Next you can communicate with OpenHexa, for example:

```
dagRun.log_message(priority="INFO", message="Setup [done], start processing")
dagRun.progress_update(progress=10)
[...]
dagRun.progress_update(progress=100)
dagRun.add_outputfile(title="Wonderfull Data", uri="s3://nice-bucket/prod-pipelines/output.csv")
```
