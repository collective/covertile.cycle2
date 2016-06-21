*** Settings ***

Resource  collective/cover/tests/cover.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${carousel_tile_location}  "covertile.cycle2.carousel"
${document_selector}  //div[@id="content-trees"]//li[@class="ui-draggable"]/a[@data-ct-type="Document"]/span[text()='My document']/..
# Previously using "span[text()='my-image1']" below, but image was reindexed in testing.py so real title is now shown
${image_selector1}  //div[@id="content-trees"]//li[@class="ui-draggable"]/a[@data-ct-type="Image"]/span[text()='Test image #1']/..
# ${slide1}  //div[@data-cycle-title='Test image #1'][contains(@class,"cycle-slide-active")]
${slide1}  div.cycle-slide-active[data-cycle-title="Test image #1"]
${image_selector2}  //div[@id="content-trees"]//li[@class="ui-draggable"]/a[@data-ct-type="Image"]/span[text()='Test image #2']/..
# ${slide2}  //div[@data-cycle-title='Test image #2'][contains(@class,"cycle-slide-active")]
${slide2}  div.cycle-slide-active[data-cycle-title="Test image #2"]
# ${slide2_updated}  //div[@data-cycle-title='New Title'][contains(@class,"cycle-slide-active")]
${slide2_updated}  div.cycle-slide-active[data-cycle-title="New Title"]

${tile_selector}  div.tile-container div.tile
${autoplay_id}  covertile-cycle2-carousel-autoplay-0
${edit_link_selector}  a.edit-tile-link

*** Keywords ***

Get Total Carousel Images
    [Documentation]  Total number of images in carousel is stored in this
    ...              element
    # Note: we are a bit lazy about adding concat here, but then how long do you want this line to be?
    ${return} =  Get Matching XPath Count  //div[contains(@class,"covertile-cycle2")]//div[contains(concat(" ", @class," "), " slide ") and not(contains(@class, "sentinel"))]
    [Return]  ${return}

*** Test cases ***

Test Carousel Tile

    Enable Autologin as  Site Administrator
    Go to Homepage
    Create Cover  Title  Description

    # add a carousel tile to the layout
    Open Layout Tab
    Add Tile  ${carousel_tile_location}
    
    # Set the image size to original
    Click Element  css=a.config-tile-link
    Wait Until Element Is Visible  css=select#covertile-cycle2-carousel-image-imgsize
    Select From List  css=select#covertile-cycle2-carousel-image-imgsize  _original
    Click Button  Save
    Save Cover Layout

    # as tile is empty, we see default message
    Compose Cover
    Page Should Contain  This carousel is empty; open the content chooser and drag-and-drop some items here.

    # drag&drop an Image
    Open Content Chooser
    Click Element  link=Content tree
    Drag And Drop  xpath=${image_selector1}  css=${tile_selector}
    Wait Until Page Contains Element  css=${slide1}
    Sleep  1s  Wait for Cycle2 to load overlay
    Page Should Contain  This image #1 was created for testing purposes
    # we have 1 image in the carousel
    ${images} =  Get Total Carousel Images
    Should Be Equal  '${images}'  '1'

    # move to the default view and check tile persisted
    Click Link  link=View
    Wait Until Page Contains Element  css=${slide1}
    Sleep  1s  Wait for Cycle2 to load overlay
    Page Should Contain  This image #1 was created for testing purposes

    # drag&drop another Image
    Compose Cover
    Open Content Chooser
    Click Element  link=Content tree

    Drag And Drop  xpath=${image_selector2}  css=${tile_selector}
    # Need to change view before second image is loaded

    # move to the default view and check tile persisted
    Click Link  link=View
    Wait Until Page Contains Element  css=${slide2}
    Sleep  1s  Wait for Cycle2 to transition
    Page Should Contain  This image #2 was created for testing purposes
    # we now have 2 images in the carousel
    ${images} =  Get Total Carousel Images
    Should Be Equal  '${images}'  '2'

    # drag&drop an object without an image: a Page
    Compose Cover
    Sleep  1s  Wait for carousel to load
    Open Content Chooser
    Click Element  link=Content tree
    
    Drag And Drop  xpath=${document_selector}  css=${tile_selector}

    # Any content without an image is silently ignored, so we should not see the Document
    Click Link  link=View
    Sleep  2s  Wait for Carousel to load
    Page Should Not Contain  This document was created for testing purposes


    ### Test Custom Title functionality

    Click Link  link=View
    Wait Until Page Contains Element  css=${slide1}
    Sleep  1s  Wait for Cycle2 to load overlay
    Element Should Contain  xpath=//div[@class='cycle-overlay']  Test image #1

    # Go to the right
    Click Element  xpath=//div[@class='cycle-next']
    Wait Until Page Contains Element  css=${slide2}
    Sleep  1s  Wait for Cycle2 to transition
    Element Should Contain  xpath=//div[@class='cycle-overlay']  Test image #2

    # Set custom Title
    Compose Cover
    Click Link  css=${edit_link_selector}
    Wait Until Element Is Visible  css=input.custom-title-input
    Input Text  xpath=//div[contains(@class,"textline-sortable-element")][2]//input[@class='custom-title-input']  New Title
    Click Button  Save
    Sleep  2s  Wait for carousel to load

    Click Link  link=View
    Wait Until Page Contains Element  css=${slide1}
    Sleep  1s  Wait for Cycle2 to load overlay
    Element Should Contain  xpath=//div[@class='cycle-overlay']  Test image #1

    # Go to the right
    Click Element  xpath=//div[@class='cycle-next']
    # Test modified Title
    Wait Until Page Contains Element  css=${slide2_updated}
    Sleep  1s  Wait for Cycle2 to transition
    Element Should Contain  xpath=//div[@class='cycle-overlay']  New Title


    ### Test Custom Description functionality

    # Set custom Description & custom URL
    Compose Cover
    Click Link  css=${edit_link_selector}
    Wait Until Element Is Visible  css=textarea.custom-description-input
    Input Text  xpath=//div[contains(@class,"textline-sortable-element")][1]//textarea[@class='custom-description-input']  New Description
    Input Text  xpath=//div[contains(@class,"textline-sortable-element")][1]//input[@class='custom-url-input']  http://www.google.com
    Click Button  Save
    Sleep  2s  Wait for carousel to load

    # Test modified Description & URL
    Click Link  link=View
    Wait Until Page Contains Element  css=${slide1}
    Sleep  1s  Wait for Cycle2 to load overlay
    Element Should Contain  xpath=//div[@class='cycle-overlay']  New Description
    ${image_url} =  Get Element Attribute  css=div.cycle-slide a@href
    Should Be Equal  ${image_url}  http://www.google.com/


    ## Test carousel autoplay
    # initially enabled
    Page Should Contain Element  xpath=//div[contains(@class,"covertile-cycle2") and @data-cycle-paused="false"]

    # edit the tile
    Compose Cover
    Click Link  css=${edit_link_selector}
    Wait Until Element Is Visible  ${autoplay_id}
    # disable carousel autoplay
    Unselect Checkbox  ${autoplay_id}
    Click Button  Save

    # carousel autoplay is now disabled. Sometimes we need to reload the page.
    Reload Page
    Page Should Contain Element  xpath=//div[contains(@class,"covertile-cycle2") and @data-cycle-paused="true"]


    ## Test customized overlay
    Open Layout Tab
    Click Element  css=a.config-tile-link
    Wait Until Element Is Visible  css=textarea#covertile-cycle2-carousel-overlay-template
    Input Text  css=textarea#covertile-cycle2-carousel-overlay-template  <div>What a nice overlay</div>
    Click Button  Save

    # Overlay should be same as configured above
    Click Link  link=View
    Wait Until Page Contains Element  css=div.cycle-overlay div
    Element Should Contain  xpath=//div[@class='cycle-overlay']  What a nice overlay


    ## Test selecting thumbnail pager
    # Check default pager is "dots"
    Page Should Contain Element  css=div.cycle-pager > span.cycle-pager-active
    # And that thumbnails are therefore NOT generated
    Page Should Not Contain Element  xpath=//div[@data-thumbnail]

    Open Layout Tab
    Click Element  css=a.config-tile-link
    Wait Until Element Is Visible  css=select#covertile-cycle2-carousel-pager-style
    Select From List  css=select#covertile-cycle2-carousel-pager-style  thumbnails_square
    Click Button  Save

    # Test thumbnail pager in place
    Compose Cover
    Page Should Contain Element  css=div.cycle-pager > a > img


    # delete the tile
    Open Layout Tab
    Delete Tile
    Save Cover Layout
