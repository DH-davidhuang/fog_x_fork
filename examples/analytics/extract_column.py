import fog_x

dataset = fog_x.dataset.Dataset(
    name="demo_ds",
    path="~/test_dataset",
)

dataset.load_rtx_episodes(
    name="berkeley_autolab_ur5",
    split="train[:5]",
)

all_step_data = dataset.get_step_data() # get lazy polars frame of the entire dataset
id_to_language_instruction = (
    all_step_data
    .select("episode_id", "natural_language_instruction") # only interested in episode id and language column
    .group_by("episode_id") # group by unqiue language ids, since language instruction is stored for every step
    .last()  # since instruction is same for all steps in an episode, we can just take the last one
    .collect() # the frame is lazily evaluated if we call collect() 
)

# join with the trajectory metadata 
dataset.get_episode_info().join(id_to_language_instruction, on="episode_id")
