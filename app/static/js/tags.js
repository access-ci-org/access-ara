//Declare tagify variables
export var fieldTagify, addFieldTagify, softwareTagify, addSoftwareTagify;

/* #################################
!!! DO NOT USE JQUERY WITH TAGIFY !!! 
   ################################ */

//Collect whitelist from ajax call
var fieldWhitelist = await getFieldWhitelist();
var softwareWhitelist = await getSoftwareWhitelist();

//Find user input in research field question
var fieldInput = document.querySelector("input[id=field-text-input]");
fieldTagify = new Tagify (fieldInput, {
    enforceWhitelist: true,
    whitelist: fieldWhitelist,
    editTags: false,
    dropdown:{
        enabled: 0,
        maxItems: 10,
        highlightFirst: true
        }
});

//Create tagify input for "add research fields" question
var addFieldInput = document.querySelector("input[id=field-add-tag");
addFieldTagify = new Tagify(addFieldInput, {
    blacklist: fieldWhitelist,
    editTags: false
});

//Find user input in software question
var softwareInput = document.querySelector("input[id=software-text-input]");
softwareTagify = new Tagify (softwareInput, {
    enforceWhitelist: true,
    whitelist: softwareWhitelist,
    editTags: false,
    dropdown: {
        enabled: 0,
        maxItems: 10,
        highlightFirst: true
    }
});

//Create tagify input for "add software/packages" question
var addSoftwareInput = document.querySelector("input[id=software-libraries-add-tag]");
addSoftwareTagify = new Tagify(addSoftwareInput, {
    blacklist: softwareWhitelist,
    editTags: false
});

//grab whitelist for research fields tags via AJAX
async function getFieldWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_research_fields"
    });
}

// grab whitelist for software tags via AJAX
async function getSoftwareWhitelist(){
    return await $.ajax({
        type: "GET",
        url: "/get_software",
    });
}

export function hideAddField(){
    if (addFieldTagify.getTagElms().length == 0){
        $(".hide-add-field").addClass('d-none').hide();
    }
}

export function showAddField(e){
    addFieldTagify.addTags(e.detail.data.value);
    $(".hide-add-field").removeClass('d-none').show();
}

export function hideAddSoftware(){
    if (addSoftwareTagify.getTagElms().length == 0){
        $(".hide-add-software").addClass('d-none').hide();
    }
}

export function showAddSoftware(e){
    addSoftwareTagify.addTags(e.detail.data.value);
    $(".hide-add-software").removeClass('d-none').show()
}

export function fieldInWhitelist(e){
    let tagValues = fieldTagify.value;
    let duplicate = false;

    for(let i=0; i < tagValues.length; i++){
        if (e.detail.data.value.toLowerCase() === tagValues[i].value.toLowerCase()){
            duplicate = true;
        }
    }

    if (!duplicate){
        fieldTagify.addTags(e.detail.data.value);
    }
}

export function softwareInWhitelist(e){
    let tagValues = softwareTagify.value;
    let duplicate = false;

    for(let i=0; i < tagValues.length; i++){
        if (e.detail.data.value.toLowerCase() === tagValues[i].value.toLowerCase()){
            duplicate = true;
        }
    }

    if (!duplicate){
        softwareTagify.addTags(e.detail.data.value);
    }
}