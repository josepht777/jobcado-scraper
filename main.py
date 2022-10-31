from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from spider import vn_applycv_com
from spider import vietnocv_io
from spider import jobsgo
from spider import vietnamworks
from spider import topcv
from spider import careerlink_jobs
from spider import timviec
from spider import careerbuilder
from spider import timviecnhanh
from spider import timviec365
import threading
import time
options = Options()
options.headless = True
browser = webdriver.Firefox(options = options,
    executable_path = GeckoDriverManager().install())

search_terms_list = [
"",
" ",
# "Kỹ sư phần mềm C/C++",
"Kỹ sư phần mềm",
"Kỹ sư an ninh thông tin",
"Lập trình viên",
"Quản lý rủi ro ",
"Nhân viên IT hardware",
"Chuyên viên IT",
"Chuyên viên công nghệ thông tin",
"Quản lý sản phẩm",
"Chuyên viên SEO",
"Dịch vụ ứng dụng",
"Quản lý vận hành cơ sở dữ liệu",
"Quản lý dự án",
"Chuyên gia quản lý dự án",
"Thiết kế UI/UX",
"Kỹ sư kiểm thử phần mềm",
"Phân tích nghiệp vụ",
"Chuyên gia phân tích nghiệp vụ",
"Kỹ sư hệ thống",
"Kỹ sư ứng dụng an toàn thông tin",
"Thiết kế đồ hoạ",
"Chuyên viên triển khai phần mềm",
"Chuyên viên đảm bảo an ninh",
"Chuyên gia kiến trúc công nghệ thông tin",
"Chuyên gia an ninh mạng",
"Kiến trúc sư nghiệp vụ",
"Chuyên gia kiến trúc tích hợp",
"Chuyên viên quản lý, vận hành các hệ thống mạng viễn thông",
"Chuyên viên  triển ứng dụng",
"Kỹ sự giải pháp",
"Kỹ sư dữ liệu",
"Chuyên gia nghiên cứu xử lý ngôn ngữ tự nhiên",
"Chuyên viên bán hàng dự án công nghệ thông tin",
"Chuyên  tư vấn giải pháp và quản lý dự án",
"Programming",
"software engineer",
"API",
"Oracle",
"JIRA",
"Project management",
"Agile software development",
"Agile",
"JavaScript",
"Java",
"React",
"Vue",
"AWS",
"Vietnam",
"tiếp viên hàng không",
"quản lý",
"kế toán",
"dược sĩ",
"tiểu thuyết gia",
"họa sĩ",
"người giúp việc",
"nhạc sĩ",
"nông dân",
"bác sĩ",
"nha sĩ",
"học sinh",
"sinh viên",
"luật sư",
"cảnh sát",
"kỹ sư",
"y tá",
"nhân viên vệ sinh",
"nhân viên văn phòng",
"phi công",
"phi hành gia",
"bảo vệ",
"nhà khoa học",
"đầu bếp",
"thợ cắt tóc",
"thẩm phán",
]


#Multi-threading
list_of_functions = [
    vietnamworks.run,
    timviec365.run,
    topcv.run,
    jobsgo.run,
    timviec.run,
    timviecnhanh.run,
    careerlink_jobs.run,
    vn_applycv_com.run,
    # vietnocv_io.run #requires login
    # careerbuilder.run #ip blocked
    ]

try:
    thread_list = []
    for f in list_of_functions:
        x = threading.Thread(target=f, args=(browser, search_terms_list))
        thread_list.append(x)

    for thread in thread_list:
        thread.start()
finally:
    print('Finished')
    time.sleep(24 * 60 * 60)

# Single-threading
# while True:
    # try:
    #     # timviec365.run(browser, search_terms_list)
    #     print('start vn_applycv_com')
    #     # vn_applycv_com.run(browser)
    #     print('finish vn_applycv_com')
    # finally:
    #     # time.sleep(24 * 60 * 60)
    #     try:
    #         print('timviecnhanh start')
    #         # timviecnhanh.run(browser, search_terms_list)
    #         print('timviecnhanh finish')
    #     finally:
    #         try:
    #             print('careerlink start')
    #             # careerlink_jobs.run(browser, search_terms_list)
    #             print('careerlink finish')
    #         finally:
    #             try:
    #                 print('start topcv')
    #                 # topcv.run(browser, search_terms_list)
    #                 print('finish topcv')
    #             finally:
    #                 try:
    #                     print('timviec start')
    #                     # timviec.run(browser, search_terms_list)
    #                     print('timviec finish')
    #                 finally:
    #                     try:
    #                         print('start jobsgo')
    #                         # jobsgo.run(browser, search_terms_list)
    #                         print('finish jobsgo')
    #                     finally:
    #                         try:
    #                             print('start vietnocv_io')
    #                             # Requires login, currently we have no login system that would not be tracked but we could create a junk email for a one off.
    #                             # vietnocv_io.run(browser, search_terms_list)
    #                             print('finish vietnocv_io')
    #                         finally:
    #                             try:
    #                                 print('start vietnamworks')
    #                                 vietnamworks.run(browser, search_terms_list)
    #                                 print('finish vietnamworks')
    #                             finally:
    #                                 try:
    #                                     print('careerbuilder start')
    #                                     # careerbuilder.run(browser, search_terms_list.reverse())
    #                                     print('careerbuilder finish')
    #                                 finally:
    #                                     time.sleep(24 * 60 * 60)