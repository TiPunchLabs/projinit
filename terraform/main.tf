resource "github_repository" "projinit" {
  name        = "projinit"
  description = "CLI pour initialiser, auditer et mettre à jour des projets selon des standards définis"
  visibility  = "public"
  auto_init   = false

  # Features
  has_issues   = true
  has_wiki     = false
  has_projects = false

  # Settings
  allow_merge_commit     = true
  allow_squash_merge     = true
  allow_rebase_merge     = true
  delete_branch_on_merge = true

  # Topics
  topics = [
    "cli",
    "python",
    "project-generator",
    "standards",
    "automation",
    "devtools"
  ]

  # License already in repo
  license_template = null
}