<!--
SPDX-FileCopyrightText: 2022 - 2023 Orthanc Team SRL <info@orthanc.team>

SPDX-License-Identifier: CC-BY-4.0
-->

# Purpose

This is a sample setup to demonstrate how to share publication links granting access to a single study.
This setup uses Keycloak to authenticate users, integrates with [MedDream](https://www.softneta.com/products/meddream-dicom-viewer/) viewer.
This setup also integrate an Orthanc that can be used by api clients (using basic auth).

# Description

This demo contains:

- an `orthanc` container accessible by logged in users and used for publication links.
- an `orthanc-for-api` container accessible in basic auth (mainly used for scripts and/or DicomWEB clients).  Is is also used by MedDream.
- an `orthanc-db` container to handle the orthanc postgreSQL database.
- an `orthanc-auth-service` container that generates and validates tokens + interfaces with Keycloak.
- an `orthanc-keycloak` container that handles users and roles.
- a `keycloak-db` container to handle the keycloak postgreSQL database.
- a `meddream-viewer` container to run MedDream.
- a `meddream-token-service` container to generate/validate tokens for MedDream accesses.
- an `orthanc-nginx` container acting as a reverse proxy in front of the other containers.

# Warning

**Disclaimer**: this sample is provided 'as is' without any guarantee.  Don't use it in production unless you perfectly understand every part of it.

Before you use it in production make sure to update all hardcoded passwords and secret keys (search for `change-me`).

# Starting the setup

To start the setup, type: `docker compose up`.  Some containers will restart multiple times while waiting for the Keycloak container to be ready.

# demo

## As an admin user

- Open the Orthanc UI at [http://localhost/orthanc/ui/app/](http://localhost/orthanc/ui/app/) (login/pwd: `admin`/`change-me`)
- upload a dicom file in Orthanc
- you may click `view the study in MedDream`
- On the uploaded file, click on the `Share` button and then on `Share` in the dialog box and then on `Copy and close`
- Keep the link in your clipboard.  You may share this link with an external user.
- Go to `Profile` -> `Logout`

## As a guest user

- Open a new private browser window or open another browser
- paste the link in the address bar
- this will open the MedDream Viewer on the specific study but the guest user won't have access to other resources in Orthanc.

## As a doctor user

- Open the Orthanc UI at [http://localhost/orthanc/ui/app/](http://localhost/orthanc/ui/app/) (login/pwd: `doctor`/`change-me`)
- The doctor user is a restricted user who can browse the whole set of studies but who can not upload/modify/delete them.

## As an external user

- On another Orthanc e.g, the one running everyday on your machine, add a new DicomWeb server:
  ```
  {
      "DicomWeb" : {
          "Servers" : {
                "auth-service-demo": {
                "Url": "http://localhost/orthanc-api/dicom-web/",
                "Username": "dicom-web-client-user",
                "Password": "change-me"
            }
     }
  }
  ```
- Restart it
- Browse your local Orthanc instance and, on a study, click `SendTo -> Dicom WEB Servers -> auth-service-demo`
- Check the study has been received in the demo Orthanc by logging in as the doctor user again