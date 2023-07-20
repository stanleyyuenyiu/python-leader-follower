# python-leader-follower
Python base leader follower application with zoo-keeper integrate

- when a leader alive, follower would not process any action
- when a leader failure, follower will promote as leader
- when the leader back from failure, it will become follower

#### Prerequisite
- python: 3.0
- docker
- make

### How to start

1. Start zoo keeper
```
make zk-up
```

2. Install
```
make setup
```

3. start leader
```
make start-leader
```

4. start follower (in other terminal)
```
make start-follower
```