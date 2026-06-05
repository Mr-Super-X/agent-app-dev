"""冒烟测试：验证 JSON mode 调用能 mock 通。"""
from unittest.mock import patch, MagicMock

from app.stable_output import extract_person


def test_extract_person_parses_json():
    """冒烟测试：mock OpenAI 返回 JSON，验证解析。"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"name": "小明", "age": 25}'))]

    with patch("app.stable_output.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        result = extract_person("小明今年 25 岁")
        assert result == {"name": "小明", "age": 25}
