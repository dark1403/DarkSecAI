from .dast import create_dast_analysis_prompt
from .sast import create_sast_analysis_prompt, create_sast_deep_analysis_prompt
from .consolidation import create_consolidation_prompt
from .deep_analysis import create_deep_analysis_prompt
from .dom_xss import create_dom_xss_pathfinder_prompt
from .file_upload import create_file_upload_analysis_prompt
from .headers import create_headers_analysis_prompt
from .js_recon import create_js_recon_prompt
from .jwt import create_jwt_blue_team_prompt, create_jwt_red_team_prompt
from .payload_forge import create_payload_forge_prompt
from .privesc import create_privesc_pathfinder_prompt
from .ssti import create_ssti_forge_prompt
from .validation import create_validation_prompt
from .xss import create_xss_payload_generation_prompt
from .sql import create_sqlmap_command_generation_prompt

__all__ = [
    'create_dast_analysis_prompt',
    'create_sast_analysis_prompt',
    'create_sast_deep_analysis_prompt',
    'create_consolidation_prompt',
    'create_deep_analysis_prompt',
    'create_dom_xss_pathfinder_prompt',
    'create_file_upload_analysis_prompt',
    'create_headers_analysis_prompt',
    'create_js_recon_prompt',
    'create_jwt_blue_team_prompt',
    'create_jwt_red_team_prompt',
    'create_payload_forge_prompt',
    'create_privesc_pathfinder_prompt',
    'create_ssti_forge_prompt',
    'create_validation_prompt',
    'create_xss_payload_generation_prompt',
    'create_sqlmap_command_generation_prompt',
]
