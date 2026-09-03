# GitHub Terminal Commands

```bash
cd ~/Downloads/ResilioNet_GitHub_RUN/DisasterTelecomBackupPlanner_Local

git init
git branch -M main
git add -A
git status
git commit -m "feat: add ResilioNet disaster telecom backup planner"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/shaunakmirajgaonkar/disaster-telecom-backup-planner.git
git push -u origin main
```
