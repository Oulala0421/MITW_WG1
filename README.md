# #MITW_WG1 FHIR Patient 簡介

## FHIR Patient檔案主要可依使用情境的不同，根據.json中的`"managingOrganization"`欄位分為三類：

* ### Patient ForIdentifier
`"managingOrganization":{"reference": "Organization/MITW.ForIdentifier"}`

* ## Patient ForContact
`"managingOrganization":{"reference": "Organization/MITW.ForContact"}`

* ## Patient ForPHR
`"managingOrganization":{"reference": "Organization/MITW.PHR"}`

