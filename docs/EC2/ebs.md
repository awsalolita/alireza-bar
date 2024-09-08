# attaching volume
### Mounting volume
* stop instance
* detach and attach to another ec2
* mount it 
```bash
mount /dev/sdb1 /mnt
OR
mount -t xfs -o nouuid /dev/sdb1 /mnt
```
OR 
```bash
sudo mkfs -t ext3 /dev/sdf
sudo mount /dev/sdf /mnt/data-store
echo "/dev/sdf /mnt/data-store ext3 defaults,noatime 1 2" | sudo tee -a /etc/fstab
```

# update size
```bash
sudo resize2fs /dev/nvme1n1
```

