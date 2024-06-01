# Đồ án NT208.O21.ANTN Lập trình Ứng dụng Web - Nhóm 4
## Danh sách thành viên
- Hồ Hoàng Diệp - 22520249
- Nguyễn Đặng Nguyên Khang - 22520617
- Trần Vỹ Khang - 22520628

## Hướng dẫn setup môi trường

- Install Django: ``` py -m pip install Django ``` (Tham khảo thêm tại https://docs.djangoproject.com/en/5.0/topics/install/)

- Run project:

```
git clone https://github.com/Diephho/ansaplangdaihoc.git
cd ansaplangdaihoc
py manage.py runserver
```
## Các gói phụ thuộc
- Các gói được sử dụng nằm ở file [requirement.txt](./requirement.txt)
- Để sử dụng tính năng chatAI và google maps, cần thêm vào hai biến môi trường OPENAI_API_KEY (có thể lấy key từ [openAI](https://openai.com/)) và GGMAP_API_KEY (lấy key từ google)

## Các tính năng của web
- Tính năng cơ bản
  - Đăng nhập, đăng ký sử dụng tài khoản/mật khẩu, đăng xuất, đổi mật khẩu
  - Hiển thị danh sách bài viết: Trang chủ, thể loại món, bài viết trong ngày, top xếp hạng)
  - Công cụ tìm kiếm cơ bản
  - Xem, tạo, chỉnh sửa Profile
  - Đăng bài viết
  - Bình luận, đánh giá, xóa bình luận
  - Mobile
  - Cấu hình dung lượng ảnh phù hợp với Desktop và Mobile
- Tính năng nâng cao
  - Đăng nhập bằng Google
  - Đăng nhập bằng Facebook (còn cải thiện)
  - Công cụ tìm kiếm tự động gợi ý
  - Google Maps cho đăng bài và hiển thị bài đăng
  - ChatAI (ChatGPT)
  - Xử lý không load lại trang khi bình luận, đánh giá, xóa bình luận

## Domain:
https://ansaplangdaihoc.azurewebsites.net/

## Bonus
- [Video seminar](https://www.youtube.com/watch?v=yKTFv3F8op4&t=31s)

![image](https://github.com/Diephho/WEB_WORK/assets/126962960/ead74163-8d18-4536-b34b-b554c0d3c792)

- Deploy (use Azure)
![image](https://github.com/Diephho/WEB_WORK/assets/126962960/7da5d631-7820-4198-aa4b-791881c15e39)

- Google Index
![image](https://github.com/Diephho/WEB_WORK/assets/126962960/66ae599f-39dd-494d-8e11-1ae1e5b8c5a9)

- Google Page Speed & SEO Test
![image](https://github.com/Diephho/WEB_WORK/assets/126962960/d5a80288-aefc-4b3d-96d0-9bf2e2082443)
![image](https://github.com/Diephho/WEB_WORK/assets/126962960/60f5b3e2-1d55-4bfd-aa18-26a57c7cf8f2)

- Slug
![image](https://github.com/Diephho/WEB_WORK/assets/126962960/2ce6b1e6-c93b-4776-a326-16bc96bb8ef9)



