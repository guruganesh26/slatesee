from slates.service.common import convert_base64_to_file, remove_uploaded_file, new_uuid


def upload_files(documents, school_id, is_space_available, update_used_space, is_profile=False):
    values = []
    is_uploading_file = False
    # Hanling upload
    document_names = []
    file_size = 0
    if len(documents) > 0:
        for doc in documents:
            file_size += doc[0]["file_size"]

        if is_space_available(file_size):
            is_uploading_file = True
            for doc in documents:
                file_name_parts = doc[0]["file_name"].split('.')
                name = None
                exten = None
                for index, file_name_part in enumerate(file_name_parts):
                    if index == len(file_name_parts) - 1:
                        exten = file_name_part
                    else:
                        if name is None:
                            name = file_name_part
                        else:
                            name += file_name_part
                auto_code = new_uuid()
                file_name = "%s-%s.%s" % (name, auto_code, exten)
                file_path = convert_base64_to_file(file_name, doc[0]["file_content"], school_id, is_profile)
                document_names.append(file_path)
            update_used_space(file_size)
        else:
                return "NOT_ENOUGH_SPACE"
        if is_uploading_file:
            values.append(",".join(document_names))
            values.append(file_size)
    return values