output "repository_name" {
  description = "Nom du dépôt GitHub créé"
  value       = github_repository.projinit.name
}

output "repository_url" {
  description = "URL du dépôt GitHub"
  value       = github_repository.projinit.html_url
}

output "repository_id" {
  description = "Identifiant interne GitHub du dépôt"
  value       = github_repository.projinit.node_id
}

output "clone_url" {
  description = "URL pour cloner le dépôt (SSH)"
  value       = github_repository.projinit.ssh_clone_url
}