def insert_data(topic, value):
    return f'''
    INSERT INTO admin (topic, value) VALUES ('{topic}', '{value}');
    '''