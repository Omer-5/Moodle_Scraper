# Login
HOME_PAGE_URL = "https://md.hit.ac.il/"
LOGIN_PAGE_URL = "https://is.hit.ac.il/nidp/idff/sso?id=HITUserPassword&sid=2&option=credential&sid=2&target=https%3A%2F%2Fmd.hit.ac.il%2Flogin%2Findex.php"
LOGIN_BUTTON = "/html/body/div[1]/div[2]/div/div[1]/form/input[4]"

# course_dispacher
ALL_COURSES_DIV_XPATH = "//*[@id='region-main']/div/div"
COURSE_CLASS_NAME_XPATH = "//li[@class='block-fcl__list__item block-fcl__list__item--course']"
COURSE_CHILD_TO_REMOVE_XPATH = "//span[@class='fcl-sr-text sr-only']"

# course_extractor
DIV_SECTION_XPATH = "//div[@class='content']"
# FILE_NAME_CHILD_CLASS_NAME = "//span[@class='instancename']/span" # works in browser

# section_extractor
UL_CLASS_NAME = "section"# img-text"
LI_CLASS_NAME = "activity"
# LI_XPATH = "//li[contains(@class, 'activity')]" # works in browser
FILE_LINK_CLASS_NAME = "aalink"
FILE_NAME_CLASS_NAME = "instancename"
FILE_NAME_CHILD_CLASS_NAME = "accesshide"

# Special cells
EXTRA_DETAILS_CLASS_NAME = "contentafterlink" # additional info about a file
SECTION_SUMMARY_CLASS_NAME = "summary" # additional info about a section
