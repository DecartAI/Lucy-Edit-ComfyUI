from .video_processor_node import (
    LucyEditProAPINode,
    LucyConditionConcatNode,
)

NODE_CLASS_MAPPINGS = {
    "LucyEditProAPINode": LucyEditProAPINode,
    "LucyConditionConcatNode": LucyConditionConcatNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LucyEditProAPINode": "Lucy Edit Pro - API",
    "LucyConditionConcatNode": "Lucy Condition Concat",
}
