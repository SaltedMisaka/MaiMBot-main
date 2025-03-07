def parse_cq_code(cq_code: str) -> dict:
    """
    将CQ码解析为字典对象
    
    Args:
        cq_code (str): CQ码字符串，如 [CQ:image,file=xxx.jpg,url=http://xxx]
        
    Returns:
        dict: 包含type和参数的字典，如 {'type': 'image', 'data': {'file': 'xxx.jpg', 'url': 'http://xxx'}}
    """
    # 检查是否是有效的CQ码
    if not (cq_code.startswith('[CQ:') and cq_code.endswith(']')):
        return {'type': 'text', 'data': {'text': cq_code}}
    
    # 移除前后的 [CQ: 和 ]
    content = cq_code[4:-1]
    
    # 分离类型和参数
    parts = content.split(',')
    if len(parts) < 1:
        return {'type': 'text', 'data': {'text': cq_code}}
        
    cq_type = parts[0]
    params = {}
    
    # 处理参数部分
    if len(parts) > 1:
        # 遍历所有参数
        for part in parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key.strip()] = value.strip()
    
    return {
        'type': cq_type,
        'data': params
    }

if __name__ == "__main__":
    # 测试用例列表
    test_cases = [
        # 测试图片CQ码
        '[CQ:image,summary=,file={6E392FD2-AAA1-5192-F52A-F724A8EC7998}.gif,sub_type=1,url=https://gchat.qpic.cn/gchatpic_new/0/0-0-6E392FD2AAA15192F52AF724A8EC7998/0,file_size=861609]',
        
        # 测试at CQ码
        '[CQ:at,qq=123456]',
        
        # 测试普通文本
        'Hello World',
        
        # 测试face表情CQ码
        '[CQ:face,id=123]',
        
        # 测试含有多个逗号的URL
        '[CQ:image,url=https://example.com/image,with,commas.jpg]',
        
        # 测试空参数
        '[CQ:image,summary=]',
        
        # 测试非法CQ码
        '[CQ:]',
        '[CQ:invalid'
    ]
    
    # 测试每个用例
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"输入: {test_case}")
        result = parse_cq_code(test_case)
        print(f"输出: {result}")
        print("-" * 50)

