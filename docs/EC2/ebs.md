# attaching volume

```bash
sudo mkfs -t ext3 /dev/sdf
sudo mount /dev/sdf /mnt/data-store
echo "/dev/sdf /mnt/data-store ext3 defaults,noatime 1 2" | sudo tee -a /etc/fstab
```

# update size
```bash
sudo resize2fs /dev/nvme1n1
```

# Create volumes from snapshots