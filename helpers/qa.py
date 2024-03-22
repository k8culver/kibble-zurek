# Copyright 2024 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from dwave.cloud.api import exceptions, Problems
import dimod
import minorminer

__all__ = ["create_bqm", "find_one_to_one_embedding", "get_job_status"]

def create_bqm(num_spins=500, coupling_strength=-1):
    """
    Create a BQM representing a FM chain. 

    Args:
        num_spins: Length of chain

        coupling_strength: value of J

    Returns:
        dimod BQM  
    """
    bqm = dimod.BinaryQuadraticModel(vartype='SPIN')
    for spin in range(num_spins):
        bqm.add_quadratic(spin, (spin + 1) % num_spins, coupling_strength)
    return bqm

def find_one_to_one_embedding(ising_chain_length, sampler_edgelist):
    """
    Find an embedding of chain_length=1. 

    Args:
        ising_chain_length: Length of chain

        sampler_edgelist: sampler.edgelist

    Returns:
        embedding  
    """
    bqm = create_bqm(ising_chain_length)
    for tries in range(3):
        print(f"Attempt {tries + 1} to find an embedding...")
        embedding = minorminer.find_embedding(bqm.quadratic, sampler_edgelist)  # Currently using simple minorminer `find_embedding` function
        if max(len(val) for val in embedding.values()) == 1:
            print("Found an embedding.")
            return embedding
        
    raise ValueError("Failed to find a good embedding in 3 tries")

def get_job_status(client, job_id, job_submit_time):
    """Return status of submitted job."""

    p = Problems.from_config(client.config)
    try:
        status = p.get_problem_status(job_id)
        label_time = dict(status)["label"].split("submitted: ")[1]
        if label_time == job_submit_time:
            return status.status.value
        else:
            return None
    except exceptions.ResourceNotFoundError as err:
        return None

    