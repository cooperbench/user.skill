> DEVELOPER

<image name=[Image #1]>
</image>
can you please look into https://huggingface.co/spaces/tencent/Hunyuan3D-2? 

it is mind blowing; i can upload an image, and it extracts a 3d model: [Image #1]

can you research how we could use a huggingface API for this to potentially itnegrate later on into our product to generate e.g. the assets for placing furniture etc?

not yet implement, just reserach what would be needed, how it could work with our asset library, ...

> AGENT

I’ll research the Hugging Face Space/API surface and also inspect this repo’s current asset-library shape so the integration notes map to the product instead of staying generic.

> AGENT

The Space is a Gradio app, so the likely API path is not the normal HF model inference API; it’s the Space’s generated Gradio endpoint. I’m checking the actual endpoint schema plus the repo’s `IndexAsset` / `PlaceAsset` model so the notes cover file format, metadata, and placement flow.

> AGENT

**Short Answer** Yes, this is viable for an asset-generation pipeline, but I would treat the public HF Space as a prototype path only. For product integration, the cleaner route is either a duplicated/private Hugging Face Space on paid GPU or self-hosting Tencent’s API server behind our backend. **What The HF API Gives Us** The Space is a Gradio app, and Hugging Face documents that Gradio Spaces are callable from Python, JS, or HTTP clients. The live Hunyuan3D Space exposes `/shape_generation`, which accepts: `image`, optional text prompt, optional multiview images, `steps`, `guidance_scale`, `seed`, `octree_resolution`, background removal, chunk count, random seed. It returns: `File` mesh output, viewer HTML, mesh stats JSON, and resolved seed. A Python prototype would look roughly like: ```python from gradio_client import Client, handle_file client = Client("tencent/Hunyuan3D-2") result = client.submit( caption=None, image=handle_file("chair.png"), mv_image_front=None, mv_image_back=None, mv_image_left=None, mv_image_right=None, steps=30, guidance_scale=5.0, seed=1234, octree_resolution=256, check_box_rembg=True, num_chunks=8000, randomize_seed=False, api_name="/shape_generation", ).result() ``` The public Space currently runs on ZeroGPU, so rate limits and queueing matter. Gradio specifically warns that ZeroGPU Spaces are rate-limited. The app also has texture generation disabled in the current public setup, matching your screenshot. **Best Integration Shape For Us** Our current asset library is metadata/proxy based. `AssetLibraryEntry` supports category, tags, dimensions, […]