# views.py - video streaming for python/django

def watch(request, slug):
    video = get_object_or_404(Video, slug=slug)
    video_file = video.video.open()

    range_header = request.META.get('HTTP_RANGE', None)
    if not range_header:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.title}"'
        return response

    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if not range_match:
        return HttpResponse(status=416)  # Неподдерживаемый диапазон

    # start (начало диапазона - range) expressed in BYTES
    start = int(range_match.group(1))
    end = None
    if range_match.group(2):
        # группировка за счет дефиса и круглых скобок
        # (r'bytes=(\d+)-(\d*)', range_header)
        end = int(range_match.group(2))


    video_file.seek(0, 2)  # в конец файла
    file_size = video_file.tell()
    video_file.seek(0)  # в начало файла

    if end is None or end >= file_size:
        end = file_size - 1

    length = end - start + 1
    video_file.seek(start)

    response = HttpResponse(video_file.read(length), content_type='video/mp4')
    response['Content-Disposition'] = f'inline; filename="{video.title}"'
    response.status_code = 206  
    response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
    return response
