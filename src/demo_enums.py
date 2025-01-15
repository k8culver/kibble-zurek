# Copyright 2025 D-Wave
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

from enum import Enum


class ProblemType(Enum):
    KZ = 0
    KZ_NM = 1

    @property
    def label(self):
        return {
            ProblemType.KZ: "Kibble-Zurek Mechanism",
            ProblemType.KZ_NM: "Kibble-Zurek Mechanism with Noise Mitigation",
        }[self]
