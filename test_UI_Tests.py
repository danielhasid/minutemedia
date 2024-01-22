
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
Premier_league_list = ["Fixtures","TV Schedule","Table","Arsenal","Chelsea","Liverpool",
                       "Manchester City","Manchester United","Newcastle United","Tottenham Hotspur","West Ham United","Other Clubs"]
def test_main_page(chrome_driver):
    tag_list = []
    driver = chrome_driver
    action = ActionChains(driver)
    #Test if the navigation bar elements are enable
    nav_bar = driver.find_elements(By.XPATH,"//nav[starts-with(@class,'fixedNav')]")
    for menu in nav_bar:
        assert menu.is_enabled() == True

    transfer_element = driver.find_element(By.CSS_SELECTOR, "header div:nth-child(3) div:nth-child(1)")
    action.move_to_element(transfer_element).perform()
    transfer_links = driver.find_elements(By.CSS_SELECTOR,"body div[id='mm-root'] header div div ul:nth-child(1)")
    for transfer_element in transfer_links:
        assert transfer_element.is_enabled() == True

    element = driver.find_element(By.CSS_SELECTOR, "header div:nth-child(3) div:nth-child(2)")
    action.move_to_element(element).perform()
    tag_names = driver.find_elements(By.TAG_NAME,"ul")
    for tag in tag_names:
        tag_list.append(tag.text)
        assert tag.is_enabled() == True
    assert Premier_league_list.sort() == tag_list.sort()
    assert len(tag_list) == 12



