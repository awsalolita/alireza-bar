## file storage
File storage is ideal when you require centralized access to files that need to be easily shared and managed by multiple host computers. Typically, this storage is mounted onto multiple hosts and requires file locking and integration with existing file system communication protocols.Common use cases for file storage include:
1.Large content repositories
2.Development environments
3.User home directories

# block  storage 
While file storage treats files as a singular unit, block storage splits files into fixed-size chunks of data called blocks that have their own addresses.
when you want to change a character in a file, you just change the block, or the piece of the file, that contains the character. This ease of access is why block storage solutions are fast and use less bandwidth.

Since block storage is optimized for low-latency operations, it is a typical storage choice for high-performance enterprise workloads, such as **databases** or enterprise resource planning (**ERP**) systems

# object storage 
Objects, much like files, are also treated as a single unit of data when stored. However, unlike file storage, these objects are stored in a **flat structure** instead of a hierarchy. Each object is a file with a unique identifier. This identifier, along with any additional metadata, is bundled with the data and stored.
Changing just one character in an object is more difficult than with block storage. When you want to change one character in a file, the entire file must be updated.
**you can store almost any type of data, and there is no limit to the number of objects stored, making it easy to scale. Object storage is generally useful when storing large data sets, unstructured files like media assets, and static assets, such as photos.**
