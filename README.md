# OPRF Asset Updater
A workflow which automatically updates OPRF standard asset files from the OpRedFlag repository

## Usage
### Step 1
First, update all of your OPRF asset files. This is important, because otherwise the initial run of the script could cause issues.

### Step 2
Create a file in your repository root called `oprf-versions.json`. The contents of the file should look something like this:
```json
{
  "missile-code": {
    "version": null,
    "path": "Nasal/missile-code.nas"
  },
  "damage": {
    "version": null,
    "path": "Nasal/damage.json"
  }
}
```

The keys of the JSON (in this case, "missile-code" and "damage") correspond to the ID of an OPRF asset. You can view all available options [here](https://github.com/NikolaiVChr/OpRedFlag/blob/master/versions.json).

For each of those keys, you should have a version number and a file path. The file path should be set to the location of the asset file, relative to your repository's root. For now, you can leave the "version" set to null.

### Step 3

Create a workflow file on your repository. You can use the template below. If you don't have much experience with workflows, don't worry - this file will work fine as-is.

```yaml
name: OPRF Asset Updater

on:
  # Once Daily
  schedule: 
    - cron: "0 0 * * *"
  # When the workflow is manually run
  workflow_dispatch:
    inputs:
      include:
        description: "Files to update, separated by commas."
        required: false
        default: "*"
      exclude:
        description: "Files to skip, separated by commas."
        required: false
        default: ""
      major:
        description: "Allow major updates, not recommended until after verifying compatibility"
        required: true
        default: "false"
        type: choice
        options:
          - true
          - false

jobs:
  update:
    # Needs to be a UNIX system
    runs-on: ubuntu-latest
    # Needs permission to write files in order to update them
    permissions:
      contents: write
    steps:
      - name: "Manual Update"
        uses: BobDotCom/OPRFAssetUpdater@main
        if: "${{ github.event_name == 'workflow_dispatch' }}"
        with:
          include: ${{ inputs.include }}
          exclude: ${{ inputs.exclude }}
          major: ${{ inputs.major }}
      - name: "Scheduled Update"
        uses: BobDotCom/OPRFAssetUpdater@main
        if: "${{ github.event_name != 'workflow_dispatch' }}"

```

### Step 4

Create a manual workflow run, and wait until it finishes.
<img width="1440" alt="Screenshot 2023-09-21 at 1 07 11 AM" src="https://github.com/BobDotCom/oprf-asset-updater/assets/71356958/255e8e86-719f-4996-9ecb-24b55c726615">


Once it's done, check the commit history for your repository, and make sure no incompatible changes were added in the last commit. If needed, update your aircraft to make it compatible.

### Step 5
Now your repo is set up! Once per day, your repository will check for changes from the oprf repository, and if there are any compatible changes, it will update your assets.

Occasionally, incompatible changes will be made. You should check from time to time, making sure you aren't out of date. If an incompatible change is made, you will need to make sure your aircraft is ready fo the changes, then create a manual workflow run (See [Step 4](#step-4)), and select the "major" option. 

## Advanced Usage
The following is an extended example with all available options.
```yaml
- uses: BobDotCom/oprf-asset-updater@v0.2
  with:
    # Optional. Location of OpRedFlag asset GitHub repository, in User/Repo format
    # Defaults to "NikolaiVChr/OpRedFlag"
    repository: 'BobDotCom/OpRedFlag'

    # Optional. The branch of the OpRedFlag repository to use
    # Defaults to "master"
    branch: feature-123

    # Optional. Location of local versions.json file
    # Defaults to "oprf-versions.json"
    version-file: 'data/versions.json'

    # Optional. Asset keys to update, separated by commas.
    # Defaults to all keys included in the version file (*)
    include: 'damage,missile-code,datalink'

    # Optional. Asset keys to skip, separated by commas.
    # Defaults to ""
    exclude: "station-manager,iff"

    # Optional. Allow major updates, not recommended until after verifying compatibility
    # Defaults to false
    major: true
```
