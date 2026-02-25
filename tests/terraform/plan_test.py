import subprocess
import sys

def test_terraform_plan():
    """Ensure terraform plan has no changes"""
    result = subprocess.run([
        'terraform', 'plan', '-detailed-exitcode',
        '-var-file=environments/dev/terraform.tfvars'
    ], cwd='infra', capture_output=True, text=True)
    
    assert result.returncode == 0, "Terraform plan failed"
    assert "No changes" in result.stdout, "Unexpected changes in plan"
