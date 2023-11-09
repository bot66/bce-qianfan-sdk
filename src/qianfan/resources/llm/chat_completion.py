# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

from qianfan.config import get_config
from qianfan.consts import DefaultLLMModel
from qianfan.resources.llm.base import UNSPECIFIED_MODEL, BaseResource
from qianfan.resources.typing import QfLLMInfo, QfMessages, QfResponse, QfRole


class ChatCompletion(BaseResource):
    """
    QianFan ChatCompletion is an agent for calling QianFan ChatCompletion API.
    """

    @classmethod
    def _supported_models(cls) -> Dict[str, QfLLMInfo]:
        """
        preset model list of ChatCompletion
        support model:
         - ERNIE-Bot-turbo
         - ERNIE-Bot
         - ERNIE-Bot-4
         - BLOOMZ-7B
         - Llama-2-7b-chat
         - Llama-2-13b-chat
         - Llama-2-70b-chat
         - Qianfan-BLOOMZ-7B-compressed
         - Qianfan-Chinese-Llama-2-7B
         - ChatGLM2-6B-32K
         - AquilaChat-7B

        Args:
            None

        Returns:
            a dict which key is preset model and value is the endpoint

        """
        return {
            "ERNIE-Bot-turbo": QfLLMInfo(
                endpoint="/chat/eb-instant",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "temperature",
                    "top_p",
                    "penalty_score",
                    "user_id",
                },
            ),
            "ERNIE-Bot": QfLLMInfo(
                endpoint="/chat/completions",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "temperature",
                    "top_p",
                    "penalty_score",
                    "functions",
                    "system",
                    "user_id",
                    "user_setting",
                },
            ),
            "ERNIE-Bot-4": QfLLMInfo(
                endpoint="/chat/completions_pro",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "temperature",
                    "top_p",
                    "penalty_score",
                    "functions",
                    "system",
                    "user_id",
                },
            ),
            "BLOOMZ-7B": QfLLMInfo(
                endpoint="/chat/bloomz_7b1",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "Llama-2-7b-chat": QfLLMInfo(
                endpoint="/chat/llama_2_7b",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "Llama-2-13b-chat": QfLLMInfo(
                endpoint="/chat/llama_2_13b",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "Llama-2-70b-chat": QfLLMInfo(
                endpoint="/chat/llama_2_70b",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "Qianfan-BLOOMZ-7B-compressed": QfLLMInfo(
                endpoint="/chat/qianfan_bloomz_7b_compressed",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "Qianfan-Chinese-Llama-2-7B": QfLLMInfo(
                endpoint="/chat/qianfan_chinese_llama_2_7b",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "ChatGLM2-6B-32K": QfLLMInfo(
                endpoint="/chat/chatglm2_6b_32k",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            "AquilaChat-7B": QfLLMInfo(
                endpoint="/chat/aquilachat_7b",
                required_keys={"messages"},
                optional_keys={
                    "stream",
                    "user_id",
                },
            ),
            UNSPECIFIED_MODEL: QfLLMInfo(
                endpoint="",
                required_keys={"messages"},
                optional_keys=set(),
            ),
        }

    @classmethod
    def _default_model(cls) -> str:
        """
        default model of ChatCompletion `ERNIE-Bot-turbo`

        Args:
            None

        Returns:
           "ERNIE-Bot-turbo"

        """
        return DefaultLLMModel.ChatCompletion

    def _convert_endpoint(self, model: Optional[str], endpoint: str) -> str:
        """
        convert endpoint to ChatCompletion API endpoint
        """
        return f"/chat/{endpoint}"

    def do(
        self,
        messages: Union[List[Dict], QfMessages],
        model: Optional[str] = None,
        endpoint: Optional[str] = None,
        stream: bool = False,
        retry_count: int = 1,
        request_timeout: float = 60,
        backoff_factor: float = 0,
        auto_concat_truncate: bool = False,
        **kwargs: Any,
    ) -> Union[QfResponse, Iterator[QfResponse]]:
        """
        Perform chat-based language generation using user-supplied messages.

        Parameters:
          messages (Union[List[Dict], QfMessages]):
            A list of messages in the conversation including the one from system. Each
            message should be a dictionary containing 'role' and 'content' keys,
            representing the role (either 'user', or 'assistant') and content of the
            message, respectively. Alternatively, you can provide a QfMessages object
            for convenience.
          model (Optional[str]):
            The name or identifier of the language model to use. If not specified, the
            default model is used(ERNIE-Bot-turbo).
          endpoint (Optional[str]):
            The endpoint for making API requests. If not provided, the default endpoint
            is used.
          stream (bool):
            If set to True, the responses are streamed back as an iterator. If False, a
            single response is returned.
          retry_count (int):
            The number of times to retry the request in case of failure.
          request_timeout (float):
            The maximum time (in seconds) to wait for a response from the model.
          backoff_factor (float):
            A factor to increase the waiting time between retry attempts.
          auto_concat_truncate (bool):
            If set to True, continuously requesting will be run until `is_truncated` is
            `False`. As a result, the entire reply will be returned.
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Additional parameters like `temperature` will vary depending on the model,
        please refer to the API documentation. The additional parameters can be passed
        as follows:

        ```
        ChatCompletion().do(messages = ..., temperature = 0.2, top_p = 0.5)
        ```

        """
        if isinstance(messages, QfMessages):
            kwargs["messages"] = messages._to_list()
        else:
            kwargs["messages"] = messages
        if (
            not get_config().DISABLE_EB_SDK
            and get_config().EB_SDK_INSTALLED
            and model in ["ERNIE-Bot-turbo", "ERNIE-Bot"]
        ):
            import erniebot

            erniebot.ak = self._client._auth._ak
            erniebot.sk = self._client._auth._sk
            erniebot.access_token = self._client._auth.access_token()
            # compat with eb sdk
            if model == "ERNIE-Bot":
                model = "ernie-bot-3.5"
            return erniebot.ChatCompletion.create(  # type: ignore
                model=model.lower(), stream=stream, **kwargs
            )
        resp = self._do(
            model,
            endpoint,
            stream,
            retry_count,
            request_timeout,
            backoff_factor,
            **kwargs,
        )
        if not auto_concat_truncate:
            return resp
        # continuously request for entire reply
        if stream:
            assert isinstance(resp, Iterator)
            return self._stream_concat_truncated(
                resp,
                kwargs.pop("messages"),
                model,
                endpoint,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )
        assert isinstance(resp, QfResponse)
        cur_content: str = resp["result"]
        entire_content: str = cur_content
        is_truncated: bool = resp["is_truncated"]
        msgs = copy.deepcopy(messages)
        while is_truncated:
            if isinstance(msgs, QfMessages):
                msgs.append(cur_content, QfRole.Assistant)
                msgs.append("继续", QfRole.User)
            else:
                msgs.append({"content": cur_content, "role": "assistant"})
                msgs.append({"content": "继续", "role": "user"})
            cur_content = ""
            kwargs["messages"] = msgs
            resp = self._do(
                model,
                endpoint,
                False,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )
            assert isinstance(resp, QfResponse)
            cur_content += resp["result"]
            entire_content += resp["result"]
            is_truncated = resp["is_truncated"]
            if not is_truncated:
                resp.body["result"] = entire_content
                return resp
        return resp

    def _stream_concat_truncated(
        self,
        first_resp: Iterator[QfResponse],
        messages: Union[List[Dict], QfMessages],
        model: Optional[str] = None,
        endpoint: Optional[str] = None,
        retry_count: int = 1,
        request_timeout: float = 60,
        backoff_factor: float = 0,
        **kwargs: Any,
    ) -> Iterator[QfResponse]:
        """
        Continuously do stream request for all pieces of reply.

        Parameters:
          model (Optional[str]):
            The name or identifier of the language model to use. If not specified, the
            default model is used(ERNIE-Bot-turbo).
          endpoint (Optional[str]):
            The endpoint for making API requests. If not provided, the default endpoint
            is used.
          stream (bool):
            If set to True, the responses are streamed back as an iterator. If False, a
            single response is returned.
          retry_count (int):
            The number of times to retry the request in case of failure.
          request_timeout (float):
            The maximum time (in seconds) to wait for a response from the model.
          backoff_factor (float):
            A factor to increase the waiting time between retry attempts.
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Yields:
            Iterator[QfResponse]: _description_
        """
        cur_content: str = ""
        for r in first_resp:
            cur_content += r["result"]
            yield r
        is_truncated: bool = True
        while is_truncated:
            if isinstance(messages, QfMessages):
                messages.append(cur_content, QfRole.Assistant)
                messages.append("继续", QfRole.User)
            else:
                messages.append({"content": cur_content, "role": "assistant"})
                messages.append({"content": "继续", "role": "user"})
            cur_content = ""
            kwargs["messages"] = messages
            resp = self._do(
                model,
                endpoint,
                True,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )

            for r in resp:
                cur_content += r["result"]
                is_truncated = r["is_truncated"]
                # if r["is_end"] and not is_truncated:
                #     r.body["is_end"] = False
                yield r

    async def ado(
        self,
        messages: Union[List[Dict], QfMessages],
        model: Optional[str] = None,
        endpoint: Optional[str] = None,
        stream: bool = False,
        retry_count: int = 1,
        request_timeout: float = 60,
        backoff_factor: float = 0,
        auto_concat_truncate: bool = False,
        **kwargs: Any,
    ) -> Union[QfResponse, AsyncIterator[QfResponse]]:
        """
        Async perform chat-based language generation using user-supplied messages.

        Parameters:
          messages (Union[List[Dict], QfMessages]):
            A list of messages in the conversation including the one from system. Each
            message should be a dictionary containing 'role' and 'content' keys,
            representing the role (either 'user', or 'assistant') and content of the
            message, respectively. Alternatively, you can provide a QfMessages object
            for convenience.
          model (Optional[str]):
            The name or identifier of the language model to use. If not specified, the
            default model is used(ERNIE-Bot-turbo).
          endpoint (Optional[str]):
            The endpoint for making API requests. If not provided, the default endpoint
            is used.
          stream (bool):
            If set to True, the responses are streamed back as an iterator. If False,
            a single response is returned.
          retry_count (int):
            The number of times to retry the request in case of failure.
          request_timeout (float):
            The maximum time (in seconds) to wait for a response from the model.
          backoff_factor (float):
            A factor to increase the waiting time between retry attempts.
          auto_concat_truncate (bool):
            If set to True, continuously requesting will be run until `is_truncated` is
            `False`. As a result, the entire reply will be returned.
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Additional parameters like `temperature` will vary depending on the model,
        please refer to the API documentation. The additional parameters can be passed
        as follows:

        ```
        ChatCompletion().ado(messages = ..., temperature = 0.2, top_p = 0.5)
        ```

        """
        if isinstance(messages, QfMessages):
            kwargs["messages"] = messages._to_list()
        else:
            kwargs["messages"] = messages
        if (
            not get_config().DISABLE_EB_SDK
            and get_config().EB_SDK_INSTALLED
            and model in ["ERNIE-Bot-turbo", "ERNIE-Bot"]
        ):
            import erniebot

            erniebot.ak = self._client._auth._ak
            erniebot.sk = self._client._auth._sk
            erniebot.access_token = self._client._auth.access_token()
            # compat with eb sdk
            if model == "ERNIE-Bot":
                model = "ernie-bot-3.5"
            return await erniebot.ChatCompletion.acreate(  # type: ignore
                model=model.lower(), stream=stream, **kwargs
            )
        resp = await self._ado(
            model,
            endpoint,
            stream,
            retry_count,
            request_timeout,
            backoff_factor,
            **kwargs,
        )
        if not auto_concat_truncate:
            return resp
        if stream:
            assert isinstance(resp, AsyncIterator)
            return self._async_stream_concat_truncated(
                resp,
                kwargs.pop("messages"),
                model,
                endpoint,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )

        assert isinstance(resp, QfResponse)
        cur_content: str = resp["result"]
        entire_content: str = cur_content
        is_truncated: bool = resp["is_truncated"]

        msgs = copy.deepcopy(messages)
        while is_truncated:
            if isinstance(msgs, QfMessages):
                msgs.append(cur_content, QfRole.Assistant)
                msgs.append("继续", QfRole.User)
            else:
                msgs.append({"content": cur_content, "role": "assistant"})
                msgs.append({"content": "继续", "role": "user"})
            cur_content = ""
            kwargs["messages"] = msgs
            resp = await self._ado(
                model,
                endpoint,
                stream,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )
            assert isinstance(resp, QfResponse)
            cur_content += resp["result"]
            entire_content += resp["result"]
            is_truncated = resp["is_truncated"]
            if not is_truncated:
                resp.body["result"] = entire_content
                return resp
        return resp

    async def _async_stream_concat_truncated(
        self,
        first_resp: AsyncIterator[QfResponse],
        messages: Union[List[Dict], QfMessages],
        model: Optional[str] = None,
        endpoint: Optional[str] = None,
        retry_count: int = 1,
        request_timeout: float = 60,
        backoff_factor: float = 0,
        **kwargs: Any,
    ) -> AsyncIterator[QfResponse]:
        """
        Stream concat.
        """
        cur_content: str = ""
        async for r in first_resp:
            cur_content += r["result"]
            yield r
        is_truncated: bool = True
        while is_truncated:
            if isinstance(messages, QfMessages):
                messages.append(cur_content, QfRole.Assistant)
                messages.append("继续", QfRole.User)
            else:
                messages.append({"content": cur_content, "role": "assistant"})
                messages.append({"content": "继续", "role": "user"})
            cur_content = ""
            kwargs["messages"] = messages

            resp = await self._ado(
                model,
                endpoint,
                True,
                retry_count,
                request_timeout,
                backoff_factor,
                **kwargs,
            )
            assert isinstance(resp, AsyncIterator)
            async for r in resp:
                cur_content += r["result"]
                is_truncated = r["is_truncated"]
                yield r
